# -*- coding: utf-8 -*-
# downloader

import urllib
import urllib2
import httplib
import cookielib
import gzip, cStringIO
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Downloader(object):
    
    def __init__(self):
        cookie = cookielib.MozillaCookieJar()
        #从文件中读取cookie内容到变量  
        #cookie.load("C:/Users/hp1/Desktop/weibo_crawler/cookie.txt", ignore_discard=True, ignore_expires=True)
        cookie.load("cookie.txt", ignore_discard=True, ignore_expires=True)
        #利用urllib2的build_opener方法创建一个opener
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        
        
        self.headers = {
        #'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
        #'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Connection": "keep-alive",
        "Host": "weibo.com"
        }
        self.charset = 'utf-8'
        
    def download(self, url, params=''):
        if params != '':
            encode_params = urllib.urlencode(params)
            url += encode_params
        print "url:"
        print url
        fails = 0
        while (True):
            try:
                if(fails>3):
                    print "Downloading html error occured."
                    break
                req = urllib2.Request(url, headers=self.headers) 
                result = self.opener.open(req,timeout = 10)
                text = result.read()
            except:
                fails = fails+1
            else:
                break
             #   print "Download Error Occured! "
              #  return None
        result = gzip.GzipFile(fileobj = cStringIO.StringIO(text)).read()
        content = result.decode(self.charset, 'ignore')
        content = eval("u'''" + content + "'''").encode(self.charset)
        return content
        
if __name__ == '__main__':
    downloader = Downloader()
    #url = 'http://weibo.com/u/3848638047?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=2#feedtop'
    #print downloader.download(url)
    # url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=3887737251450427&max_id=3887761943229187&page=1&__rnd=1442398727739'
    url = 'http://www.weibo.com/aj/v6/comment/big?ajwvr=6&id=3832039298207181&__rnd=1442713133489'
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test4.txt","w")
    result = downloader.download(url)
    result = result.decode('utf-8','ignore')
    w.write(result)
    w.close()
    
    