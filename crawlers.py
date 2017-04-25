import urllib.request,re,uuid,os,chardet
from collections import deque
#url= "https://www.avav67.com/htm/index.htm"
url= "https://www.avav67.com/htm/pic1/81350.htm"
#url= "https://www.avav67.com/htm/pic1/81343.htm"
urlDir= "https://www.avav67.com/htm/pic1/"
localPath='d:\\Work\\WebCrawlers\\pic\\'

#根据文件名创建文件    
def createFileWithFileName(localPathParam,fileName):  
    totalPath=localPathParam+fileName  
    if not os.path.exists(totalPath):  
        file=open(totalPath,'a+')  
        file.close()  
        return totalPath  

#生成一个文件名字符串   
def generateFileName():  
    return str(uuid.uuid1())

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%'%per)

#根据url保存图片为文件
def getAndSaveImg(imgUrl):  
    print(imgUrl)
    if( len(imgUrl)!= 0 ):  
        fileName=generateFileName()+'.jpg'  

        req=urllib.request.build_opener()
        #req=urllib.request.Request(imgUrl)
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
        urllib.request.install_opener(req)
        urllib.request.urlretrieve(imgUrl,createFileWithFileName(localPath,fileName),Schedule)  

#带有header的request
def getHtml(url):  
    req=urllib.request.Request(url)
    req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
    #req.add_header("Accept-Encoding","gzip, deflate, br"); #网页自动压缩
    #req.add_header("Content-Type","text/html;charset=utf-8"); #确认字符集
    req.add_header("Accept-Language","zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3");
    req.add_header("Connection","keep-alive");
    req.add_header("Cookie","__cfduid=d85710970946c06297ba709024e8d61ee1493027396; Hm_lvt_767e27c6fc5a7b6a90ba665ed5f7559b=1493027401; Hm_lpvt_767e27c6fc5a7b6a90ba665ed5f7559b=1493029319");
    req.add_header("Host","www.avav67.com");
    req.add_header("Upgrade-Insecure-Requests","1");
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0");
  
    content=urllib.request.urlopen(req).read()  
    htmlCharsetGuess = chardet.detect(content)
    htmlCharsetEncoding = htmlCharsetGuess["encoding"]

    return content.decode(htmlCharsetEncoding) 

#getAndSaveImg('https://img.581gg.com/picdata-watermark/a1/165/16542-1.jpg') #测试下载单张图片

for i in range(78645,82000):
    htmURL=urlDir+str(i)+'.htm';
    print(htmURL)
    data=getHtml(htmURL)
    #f=open(localPath+'sample.htm','w') #保存的目录
    #f.write(data)
    #f.close()
    #queue = deque() #保存所有的img的url
    linkre = re.compile('src="(.+?\.jpg)"')
    print('before get Image')
    for x in linkre.findall(data): #返回所有有匹配的列表
        print('get Image')
        getAndSaveImg(x);
