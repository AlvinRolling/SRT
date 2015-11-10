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
#from BeautifulSoup import BeautifulSoup


cj = cookielib.MozillaCookieJar()#cookiefilename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
# enable cookie handler

reload(sys)
sys.setdefaultencoding('utf-8')

class Account():
    def __init__(self):
        self.loginpostdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'ssosimplelogin' : '1',
            'vsnf': '1',
            'vsnval' : '',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            'encoding': 'UTF-8',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Chrome/43.0.2357.134 Safari/537.36'}
        #self.header = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
        # self.name = 'tang-zj13@mails.tsinghua.edu.cn'
        # self.pwd = '5shiTOP08'

    def getData(self,url):
        try:
            req = urllib2.Request(url)
            result = opener.open(req)
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
            
    def login(self,name,pwd):
        self.name = name
        self.pwd = pwd
        try:
            print "----------logining---------"
            prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1400822309846' % self.name
            prelogin = self.getData(prelogin_url)
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
            login = self.getData(urll)
            if(login.find('retcode=0')):
                print "---------login successful---------"
                #cj.save("C:/Users/hp1/Desktop/weibo_crawler/cookie.txt",ignore_discard=True, ignore_expires=True)
                cj.save("cookie.txt",ignore_discard=True, ignore_expires=True)
                return True
            else:
                return False
        except:
            return False



            
if __name__ == "__main__":
    print "---------weibo login-------"
    test = Account()
    test.login()
    url = 'http://weibo.com/p/1005055200197732/follow?relate=fans&page=1'
    result = test.getData(url)
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
