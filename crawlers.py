'''
Todo:
    -加入日志功能
    提取网页Title,保存图片标记
'''
import re,uuid,os,chardet,time
import urllib,urllib2
import socket

#初始化配置
urlDir= "https://www.avav67.com/htm/pic1/" #网页前缀
PIC_PATH='/home/albert/WebCrawlers/pic/' #图片保存地址
LOG_PATH='/home/albert/WebCrawlers/log/' #图片保存地址
REPEAT_TIMES=10 #网页读取的重试次数
socket.setdefaulttimeout(30) #通过设置socket实现urlretrieve超时


#取得当前时间字串
def getTimeStr():
    return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

#将str文件保存到日志中
def addLog(str):
    log.write(getTimeStr()+': ')
    log.writelines(str)
    
#生成带路径文件名，名字随机
def genFileName():  
    return PIC_PATH+str(uuid.uuid1())+'.jpg'

'''
显示下载进度
a:已经下载的数据块
b:数据块的大小
c:远程文件的大小
'''
def schedule(a,b,c):
    if c>0:
	per = 100.0 * a * b / c
	if per > 100 :
	    per = 100
    else:
	per=0
    print('%.2f%%'%per)

#根据url保存图片为文件
def getImg(imgUrl):  
    print(imgUrl)
    if( len(imgUrl)!= 0 ):  
        req=urllib2.build_opener()
        req.addheaders=[("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ("Accept-Language","zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"),
        ("Cache-Control","max-age=0"),
        ("Connection","keep-alive"),
        ("Cookie","__cfduid=ded0eaf16312b4afa0a6e39fc580dc4af1493044918"),
        ("Host","img.581gg.com"),
        ("If-Modified-Since","Sun, 25 Dec 2016 15:00:09 GMT"),
        ("If-None-Match","d111e995bf5ed21:0"),
        ("Upgrade-Insecure-Requests","1"),
        ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0")]
        urllib2.install_opener(req)
        for j in range(REPEAT_TIMES):
            try:
                urllib.urlretrieve(imgUrl,genFileName(),schedule)  
                print('load image success')
                break  #如果完成了，就不重复了。跳出循环。
            except:
                print('image try again')
                pass

#带有header的request
def getHtml(url):  
    #伪造头部建立request请求的对象
    req=urllib2.Request(url)
    req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
    req.add_header("Accept-Language","zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3");
    req.add_header("Connection","keep-alive");
    req.add_header("Cookie","__cfduid=d85710970946c06297ba709024e8d61ee1493027396; Hm_lvt_767e27c6fc5a7b6a90ba665ed5f7559b=1493027401; Hm_lpvt_767e27c6fc5a7b6a90ba665ed5f7559b=1493029319");
    req.add_header("Host","www.avav67.com");
    req.add_header("Upgrade-Insecure-Requests","1");
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0");
  
    #取得页面，带有重试功能
    for j in range(REPEAT_TIMES):
        try:
            content=urllib2.urlopen(req).read()  #取得页面对象
            print('load page success')
            break  #如果完成了，就不重复了。跳出循环。
        except:
            print('page try again..')
            pass
    htmlCharsetGuess = chardet.detect(content)  #判断页面编码
    htmlCharsetEncoding = htmlCharsetGuess["encoding"] #根据编码解码

    return content.decode(htmlCharsetEncoding) 

'''
    main program start from here
    '''
#getImg('https://img.581gg.com/picdata-watermark/a1/167/16785-1.jpg') #测试下载单张图片

#建立日志文件
logName=LOG_PATH+getTimeStr()+'.txt'
log=open(logName,'w')

#载入爬虫进度
f=open('PageFrom.txt','r')
pageFrom=f.readline()
f.close()

#顺序爬取网页
for i in range(int(pageFrom)+1,82000):
    htmURL=urlDir+str(i)+'.htm';
    print(htmURL)
    addLog(htmURL)
    data=getHtml(htmURL)
    f=open('PageFrom.txt','w')
    f.write(str(i))
    f.close()
    linkre = re.compile('src="(.+?\.jpg)"')#建立正则模式
    res=linkre.findall(data)#从网页全文中找到匹配模式的链接
    for x in res: #提取所有的图片链接
        getImg(x);
