# cnvd_fofa_gather
通过公司名称，在fofa上搜索可能存在通用产品的公司，原理是判断网站标题数目以及独立IP数达到一定条件时将该标题以及公司名称导出；如果想挖掘cnvd证书，可导出注册资金大于5000w的公司到这个脚本中进行通用系统收集。

# 该项目使用了免费代理池项目作为支撑，因为fofa短时间搜索不同关键词可能将导致延时错误，多次出现错误后fofa可能将会封锁你的IP
代理池项目地址：https://github.com/jhao104/proxy_pool
代理池简单使用：1.启动redis
               2.python proxypool.py schedule
               3.python proxypool.py server
               
 # 启动完代理池后就可以将想要搜集的公司名称导出，放到gs.txt进行搜索爬取，输出结果在company.txt
 python cnvd_fofa_gather
