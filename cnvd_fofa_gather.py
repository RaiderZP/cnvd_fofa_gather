import re
import base64
import requests
from urllib.parse import quote


requests.packages.urllib3.disable_warnings()

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
}


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHtml(urls):
    # 代理ip尝试连接次数
    print("---》》使用代理IP《《---")
    retry_count = 3
    proxy = get_proxy().get("proxy")
    proxy = {"http": "http://{}".format(proxy),
             "https": "https://{}".format(proxy)
             }

    while retry_count > 0:
        try:
            html = requests.get(urls, headers=headers, proxies=proxy, verify=False, timeout=10)
            # 使用代理访问
            return html
        except Exception as u:
            print('proxy_err:', retry_count)
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)

    # 代理池ip无法请求成功，尝试使用本地ip请求一次，提高容错率
    print('---》》使用本地IP《《---')
    try:
        html = requests.get(urls, headers=headers, verify=False)
        return html
    except Exception as u:
        print('lo_err:', u)
        return None



def fofa_search(kjgs, gs):
    url = 'https://classic.fofa.so//search//result_stats?qbase64='
    search = '"' + kjgs + '"'
    search_data_bs = str(base64.b64encode(search.encode("utf-8")), "utf-8")
    search_data_url = quote(search_data_bs)  # url编码
    urls = url + search_data_url
    # print(urls)

    result = getHtml(urls)

    while 1:
        if type(result) == type(None):
            print('空')
            result = getHtml(urls)
        if result.status_code == 200:
            # print(200)
            break
        else:
            print(result.status_code)
            # time.sleep(1)
            # proxy = get_proxy().get("proxy")
            result = getHtml(urls)

    results = result.content.decode('utf-8')
    # print(results)

    # 获取独立IP总数
    # print(results)
    # (1)截取ip_count = 后的内容
    ip_count_start = re.search('ip_count = ', results).span()[1]
    ip_data = results[ip_count_start:]

    # (2)匹配ip_count = 后第一次出现的数，即独立ip
    ip_count = re.match(r'\d+', ip_data).group()  # group()获取匹配到的值
    print(kjgs + "--->独立总数IP:" + ip_count)

    if int(ip_count) > 20:
        # 获取首个标题
        title_data1 = results[:ip_count_start]
        title_data2_start = re.search('网站标题排名', title_data1).span()[1]
        title_data2 = title_data1[title_data2_start:]
        # print(title_data2)
        # print(title_start)
        title_data3 = re.search('<a.*">', title_data2).group()
        title_data3_start = re.search('<a.*">', title_data2).group()[0]
        # print(title_data3)
        # 如果需要匹配一个转义字符，需要用3条反斜杠，python转义一次，正则转义一次
        title_data4_start = re.search('<\\\/a>', title_data3).span()[0]
        title_data5 = title_data3[:title_data4_start]
        title_data5_start = re.search('>', title_data5).span()[1]
        title = title_data3[title_data5_start:title_data4_start]

        # 获取首个标题对应的站点数
        num_flag1 = re.search('<span >', title_data3).span()[1]
        num_flag2 = re.search('<\\\/span>', title_data3).span()[0]
        num = title_data3[num_flag1:num_flag2]

        if int(num) > 15 or int(ip_count) >= 300:
            print("------>>标题榜首:" + title + "---->>对应条数：" + num)
            with open(r'company.txt', 'a+') as f:
                f.write(kjgs + '/' + gs + "-->独立总数IP:" + ip_count + "->标题榜首:" + title + "->标题对应数：" + num)
                f.write('\n')
                f.write('\n')
                f.close()



if __name__ == '__main__':
    # fofa_search("科技")
    # 打开公司列表，获取公司名称
    print("开始收集--------")
    for f in open('gs.txt', 'rb'):
        gs = str(f, "utf-8")
        gs = gs.strip()

        # 获取科技前面的字段
        try:
            if re.search(r'科技', gs):
                start = re.search(r'科技', gs).span()[1]
                kj = gs[:start]

                # 去除括号内容
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last, gs)
                    # q.put(kj_last)
                else:
                    fofa_search(kj, gs)
                    # q.put(kj)

            elif re.search(r'技术', gs):
                start = re.search(r'技术', gs).span()[1]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last, gs)
                    # q.put(kj_last)
                else:
                    fofa_search(kj, gs)
                    # q.put(kj)

            elif re.search(r'软件', gs):
                start = re.search(r'软件', gs).span()[1]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last, gs)
                    # q.put(kj_last)
                else:
                    fofa_search(kj, gs)
                    # q.put(kj)

            elif re.search(r'股份', gs):
                start = re.search(r'股份', gs).span()[0]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last, gs)
                    # q.put(kj_last)
                else:
                    fofa_search(kj, gs)
                    # q.put(kj)

            elif re.search(r'有限', gs):
                start = re.search(r'有限', gs).span()[0]
                kj = gs[:start]
                if '(' in kj:
                    start = re.search(r'\(', kj).span()[0]
                    end = re.search(r'\)', kj).span()[1]

                    kj_last = kj.replace(kj[start:end], '')

                    fofa_search(kj_last, gs)
                    # q.put(kj_last)
                else:
                    fofa_search(kj, gs)
                    # q.put(kj)

            else:
                if '(' in gs:
                    start = re.search(r'\(', gs).span()[0]
                    end = re.search(r'\)', gs).span()[1]

                    gs_last = gs.replace(gs[start:end], '')

                    fofa_search(gs_last, gs)
                    # q.put(kj_last)
                else:
                    kj = gs
                    # print(kj,gs)
                    fofa_search(kj, gs)
                    # q.put(kj)
        except Exception as u:
            print('main_err:', u)
