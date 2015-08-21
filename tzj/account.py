# -*- coding: utf-8 -*-
import re
import urllib
import urllib2
import rsa
import base64
import cookielib
import sys
import binascii
import os
import json
from bs4 import BeautifulSoup

# = 'cookie.txt'
cj = cookielib.MozillaCookieJar()#cookiefilename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

reload(sys)
sys.setdefaultencoding('utf-8')

# used to handle cookie

class Account():
    def __init__(self):
        self.loginpostdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'ssosimplelogin' : '1',
            #'pagerefer': '',
            #'pcid': '',
            #'door': '',  # 验证码
            
            'vsnf': '1',
            'vsnval' : '',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            #'sr': '',
            'encoding': 'UTF-8',
            #'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Chrome/43.0.2357.134 Safari/537.36'}
        #self.header = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
        self.name = '595463155@qq.com'
        self.pwd = '5shiTOP08'

    def getData(self,url):
        try:
            req = urllib2.Request(url)
            result = opener.open(req)
            #result = urllib2.urlopen(req)
            text = result.read()
            return text
        except Exception, e:
            print 'Error,url:'+url
            print e
    
    def postData(self,url,data,header):
        try:
            data = urllib.urlencode(data)
            req = urllib2.Request(url,data,header)
            result = opener.open(req)
            text = result.read()
            return text
        except Exception, e:
            print 'Error,url:'+url
            
    def login(self):
        print "----------logining---------"
        prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1400822309846' % self.name
        prelogin = self.getData(prelogin_url)
        print "prelogin: "
        print prelogin
        servertime = re.findall('"servertime":(.+?),',prelogin)[0]
        pubkey = re.findall('"pubkey":"(.+?)",',prelogin)[0]
        rsakv = re.findall('"rsakv":"(.+?)",',prelogin)[0]
        nonce = re.findall('"nonce":"(.+?)",',prelogin)[0]
        
        su = base64.b64encode(urllib.quote(self.name))
        rsaPublickey = int(pubkey,16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) +'\t'+ str(nonce) +'\n'+ str(self.pwd)
        sp = binascii.b2a_hex(rsa.encrypt(message,key))
        # encode the nickname and password
        
        self.loginpostdata['su'] = su
        self.loginpostdata['servertime'] = servertime
        self.loginpostdata['sp'] = sp
        self.loginpostdata['nonce'] = nonce
        self.loginpostdata['rsakv'] = rsakv
        
        s = self.postData('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',self.loginpostdata,self.header)
        #try:
        #urll = re.findall("location.replace\(\'(.*?)\'\);", s)[0]
        btag = 'location.replace("'
        etag = '");'
        bpos = s.find(btag)
        if bpos != -1:
            bpos += len(btag)
            epos = s.find(etag, bpos)
        else:
            bpos = s.find(btag.replace('"', "'")) + len(btag)
            epos = s.find(etag.replace('"', "'"), bpos)
        urll = s[bpos:epos]
        print "urll: ",urll
        login = self.getData(urll)
        print "successful"
        #print self.getData('http://weibo.com')
        #print self.getData('http://weibo.com/2198840781/profile?rightmod=1&wvr=6&mod=personinfo')
        '''
        except Exception, e: 
            print "failed"
            print e
            exit(0)
        '''
            
if __name__ == "__main__":
    print "---------weibo login-------"
    test = Account()
    test.login()
    url = 'http://weibo.com/p/1005055200197732/follow?relate=fans&page=1'
    #result =  test.getData(url)
    cookie ='SINAGLOBAL=1741986363194.8828.1402790278112; __gads=ID=c89a3aae13e8c3fb:T=1439276319:S=ALNI_Ma4dDrxRssSQmWPGRnmbUMuXggH2g; myuid=2198840781; un=595463155@qq.com; SUS=SID-2198840781-1440135887-GZ-fwt4s-9ad804d71331e24a2e4550bf79d07acd; SUE=es%3Dce3f1628039230c04fae251b87f4a099%26ev%3Dv1%26es2%3D745e8051739fa23648c9c8c67b300851%26rs0%3Dnnumm2cGDAeerZ7Th469P6C1gbEoAZCbG1GiQLrSku39pFW7%252B7LUNoMRGXMtfq7ELswmVznFzBG8zJGbxHLFMLUgzj5s72xcg7t3IjNgQ2O14SddeH4D6%252FEL7ASks6zDnjKGWZZz5hLFfKZERmv2Vs95yTzpkF6gJC6yZM1RJq4%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1440135887%26et%3D1440222287%26d%3Dc909%26i%3D7acd%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2198840781%26name%3D595463155%2540qq.com%26nick%3D%25E6%2589%2580%25E6%259C%2589%25E6%25B5%2581%25E6%25B5%25AA%25E7%259A%2584%25E7%25BB%2588%25E7%2582%25B9%26fmp%3D%26lcp%3D2012-01-18%252012%253A13%253A29; SUB=_2A2540sqfDeTxGeRP4loZ9C7Lwz2IHXVbqbtXrDV8PUNbu9BeLUP6kW81jXvsyI_AnRtah0w2QemcnwWnqQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56UcJIJGJ6mhRLk-T6h53C5JpX5Kzt; SUHB=0FQq6jCS5pfS_d; ALF=1471671886; SSOLoginState=1440135887; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=6845299981068.819.1440135886798; ULV=1440135886829:51:21:13:6845299981068.819.1440135886798:1440119294762' 
    '''
    from downloader import Downloader
    down = Downloader(cookie)
    result = down.download(url)
    
    '''
    #result = test.getData(url)
    header = {'cookie':cookie}
    req = urllib2.Request(url, headers=header) 
    result = urllib2.urlopen(req)
    result = result.read()
    
    result = result.decode('utf-8','ignore')
    print "result: ",result
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test1.txt","w")
    w.write(result)
    w.close()
    temp = result.replace('\\/', '/')
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test2.txt","w")
    w.write(temp)
    w.close()
    cj.save("C:/Users/hp1/Desktop/weibo_crawler/cookie.txt",ignore_discard=True, ignore_expires=True)