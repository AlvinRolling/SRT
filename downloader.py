# -*- coding: utf-8 -*-
import urllib
import urllib2
import httplib
import time
import cookielib
import gzip, cStringIO
import sys
###
reload(sys)
sys.setdefaultencoding('utf-8')
###
# 网页下载异常
class DownloadError(Exception):
    def __init__(self, url=''):
        self.error_msg = "Download %s error." % url ;

    def __str__(self):
        return repr(self.error_msg) ;


# 网页解码异常
class DecodeError(Exception):
    def __init__(self, url=''):
        self.error_msg = "Decode %s error." % url ;

    def __str__(self):
        return repr(self.error_msg) ;

#获得整个网页html内容


class Downloader():
    '''
    下载器,负责下载网页资源
    '''

    def __init__(self, cookie,charset='utf-8', timeout=10, maxtry=2):
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Connection": "keep-alive",
        "Host": "weibo.com"
        }
        self.charset = charset
        self.timeout = timeout
        self.maxtry = maxtry
	self.cookie=cookie

    def use_proxy(self, proxy):
        """
        爬虫使用代理登录,代理proxy包含代理的链接和端口格式为:http://XX.XX.XX.XX:XXXX
        """
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_support = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def use_http(self, url, params=''):
        connection = httplib.HTTPConnection('weibo.com')
        connection.request(method='GET', url=url, headers=self.headers)
        res = connection.getresponse()
        text = res.read()
        print text
        #text = gzip.GzipFile(fileobj = cStringIO.StringIO(text)).read()
        content = text.decode(self.charset, 'ignore')
        content = eval("u'''" + content + "'''").encode(self.charset)
        connection.close()
        return content

    def download(self, url, params='', try_num=0):
	
        if params != '':
            encode_params = '?' + urllib.urlencode(params)
            url += encode_params
	self.headers['cookie']=self.cookie
        req = urllib2.Request(url, headers=self.headers)
        result = urllib2.urlopen(req, timeout=self.timeout)
        text = result.read()
        content = text.decode(self.charset, 'ignore')
        print "content: ",content
        content = eval("u'''" + content + "'''").encode(self.charset)
        #raise DecodeError(url)
        #self.write('tmp.html', content)
        #content = text.decode(self.charset,'ignore')
        #content = text
        print "content: "
        print content
        return content

    def write(self, filepath, content):
        with open(filepath, 'w') as writer:
            writer.write(content)


if __name__ == '__main__':
    #from accountlib import AccountManager
    '''
    url = 'http://weibo.com/u/1309628460'
    manager = AccountManager()
    manager.init()
    manager.login()
    downloader = Downloader()
    print downloader.download(url)
    '''
    testcookie = 'SINAGLOBAL=1741986363194.8828.1402790278112; myuid=2198840781; wvr=6; __gads=ID=c89a3aae13e8c3fb:T=1439276319:S=ALNI_Ma4dDrxRssSQmWPGRnmbUMuXggH2g; un=595463155@qq.com; UOR=,,cuiqingcai.com; SUS=SID-2198840781-1439809849-GZ-fcm3a-c4e03f6f67bf39f0b13c154385d7b173; SUE=es%3D2d81508138c822751d95a683c2f02c7c%26ev%3Dv1%26es2%3De0fbf3bbbf32c85de66e7329f95361fe%26rs0%3Dk%252Bq6R02eVCEwqJkh13TA5p%252Boahm10fd5IJOkrIFbOFiXno%252BH92bLxUzF%252BXJVT%252FjpqYvPcKAM6JaUtP1C9GHqIq3dT6j%252Bl1iGM8DA7zOBI1dI0hEMw84Ya7RSTMBLxHU8zAo4LYb%252FQIoJQWRzpX5P2VUhK3OO8dMluzbuv%252Fk5NQk%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1439809849%26et%3D1439896249%26d%3Dc909%26i%3Db173%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2198840781%26name%3D595463155%2540qq.com%26nick%3D%25E6%2589%2580%25E6%259C%2589%25E6%25B5%2581%25E6%25B5%25AA%25E7%259A%2584%25E7%25BB%2588%25E7%2582%25B9%26fmp%3D%26lcp%3D2012-01-18%252012%253A13%253A29; SUB=_2A2541bFpDeTxGeRP4loZ9C7Lwz2IHXVboqWhrDV8PUNbvtBeLXPnkW9BJOHhz9QCPjv_5sCoZGTpKJZ_wQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56UcJIJGJ6mhRLk-T6h53C5JpX5KMt; SUHB=0TPEOBvhkpKBXx; ALF=1471345849; SSOLoginState=1439809849; _s_tentry=weibo.com; Apache=9734632999170.572.1439809852657; ULV=1439809852737:41:11:3:9734632999170.572.1439809852657:1439791559166'
    
    downloader = Downloader(testcookie)
    url = 'http://weibo.com/p/1005052034424692/follow?relate=fans&page=1'
    #print downloader.download(url)
    
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test4.txt","w")
    w.write(downloader.download(url))
    w.close()