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

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

reload(sys)
sys.setdefaultencoding('utf-8')

# used to handle cookie

class Account():
    def __init__(self):
        '''
        self.cur_user = ''  # 当前登录账户名
        self.pre_user = ''  # 上一个登录的账号
        self.loginpostdata = dict()
        self.accounts = list()
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        account_filepath = os.path.abspath(os.path.join(pardir, 'account.txt'))
        self.load_accounts(account_filepath)
        '''
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
        #self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '\
        #'Chrome/43.0.2357.134 Safari/537.36'}
        self.header = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
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
        login = self.getData(urll)
        print "successful"
        print self.getData('http://weibo.com')
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
    url = 'http://weibo.com/p/1005052034424692/follow?relate=fans&page=1'
    result =  test.getData(url)
    '''
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test2.txt","w")
    w.write(result.decode('utf-8'))
    w.close()
    '''
    #import gzip, cStringIO
    #result = gzip.GzipFile(fileobj=cStringIO.StringIO(result)).read()
    content = result.decode('utf-8', 'ignore')
    content = eval("u'''" + content + "'''").encode('utf-8')
    content = content.decode('utf-8', 'ignore')
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test4.txt","w")
    w.write(content)
    w.close()
    content = content.replace('\\/', '/')
    w = open("C:/Users/hp1/Desktop/weibo_crawler/test5.txt","w")
    w.write(content)
    w.close()
    soup = BeautifulSoup(content)
    print "Soup: "
    print soup.prettify()
    print "result: "
    print soup.findAll('li',attrs={'class':'follow_item S_line2'})
    