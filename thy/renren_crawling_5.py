# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import time
import os
import shutil

class SDU_Spider:
    #define characters
    def __init__(self):
        self.loginUrl = 'http://www.renren.com/PLogin.do'#login URL
        self.resultUrl = 'http://www.renren.com/353617867'#crawling URL
        self.cookieJar = cookielib.CookieJar()
        self.postdata = urllib.urlencode({#login-post-data
            'email':'haoyuetang@126.com',
            'autoLogin':'true',
            'origURL':'http://www.renren.com/home',
            'domain':'renren.com',
            'key_id':'1',
            'captcha_type':'web_login',
            'password':'5c35480601a74ad83371e9dbce045c2665e0e91af934ae7cc9e5f62d2172e4b0',
            'rkey':'44fd96c219c593f3c9612360c80310a3',
            'f':'http%3A%2F%2Fwww.renren.com%2F353617867'
        })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))

        
    def sdu_init(self):
        #初始化链接获取cookie 
        myRequest = urllib2.Request(url = self.loginUrl,data = self.postdata)     
        result = self.opener.open(myRequest)            
        result = self.opener.open(self.resultUrl)       
        # 打印返回的内容  
        # print result.read()  
        self.deal_data(result.read())
        

    def deal_data(self,myPage):
        myItems = re.finditer('share-desc',myPage,re.S)
        for item in myItems:
            temp = myPage[item.span()[1]:len(myPage)]
            stop = re.search('</p',temp,re.S)

    def get_friends(self,user_num): #获得好友列表
        user_url = 'http://friend.renren.com/friend/api/getotherfriendsdata'
        more_post = urllib.urlencode({
            "p":"{ \"fid\":\""+user_num+"\",\"pz\":\"100\",\"type\":\"WEB_FRIEND\",\"pn\":\"1\"}",
            "requestToken":"379990670",
            "_rtk":"e26730e8"})
        request = urllib2.Request(url = user_url,data = more_post)
        result = self.opener.open(request)
        result = result.read()
        friend_list = []
        page = 0
        total_str = re.findall("total\":\d*",result)
        for item in total_str:
            total = int(item[7:])
        while (page < total / 100 + 3):
            p = re.compile("fid\":\d*")
            piece = p.findall(result)
            for item in piece:
                friend_list.append(item[5:])
            more_post = urllib.urlencode({
            "p":"{ \"fid\":\"" + user_num + "\",\"pz\":\"100\",\"type\":\"WEB_FRIEND\",\"pn\":\"" + str(page) + "\"}",
            "requestToken":"379990670",
            "_rtk":"e26730e8"})
            request = urllib2.Request(url = user_url,data = more_post)
            result = self.opener.open(request).read()
            page = page + 1

        return friend_list

    def get_status(self,user_num):
        page = 0
        result = "none"  #记录搜索结果
        time_form = re.compile("dtime\":\".*?\s")
        required_time = "2015-05-29"  #记录期望搜索时间
        search = 1  #是否继续搜索
        try:
            while search:
                more_result = self.opener.open("http://status.renren.com/GetSomeomeDoingList.do?userId=" + user_num + "&curpage=" + str(page) + "&_jcb=jQuery1111031641900399699807_1433395719580&requestToken=379990670&_rtk=e26730e8&_=1433395719581")
                result = result + more_result.read()
                time = time_form.search(more_result)
                if (cmp(time.group(0)[8:],required_time) == -1) or (page > 100):  #在此之前已经没有匹配状态，自动跳出搜索
                    search = 0
                page = page + 1
        finally:
            #fp = open("user/" + user_num + ".txt",'w')
            #fp.write(result)
            #fp.close()
            return result


def extract_message(element):
    p = re.compile("rootDoingUserId")
    piece = p.split(element)
    for item in piece:
        share_type = re.search("222294044",item,re.S)#判断状态是否为需要寻找的
        if share_type:
            return 1
    return 0
        
mySpider = SDU_Spider()
mySpider.sdu_init()
searched = []
to_be_search = []
origin_user = "334135892"
to_be_search.insert(1,origin_user)
sta = mySpider.get_status("256047627")
print extract_message(sta)
searched.append(origin_user)

while len(to_be_search) > 0:
    search_user = to_be_search.pop()
    try:
        friend_list = mySpider.get_friends(search_user)
        for item in friend_list:
            if item in searched:
                continue
            searched.append(item)
            fp = open("searched.txt",'a+')
            fp.write(item)
            fp.write('\r\n')
            fp.close()
            try:
                status = mySpider.get_status(item)
                if extract_message(status):
                    to_be_search.append(item)
                    fp = open("result.txt",'a+')
                    fp.write(item)
                    fp.write('\r\n')
                    fp.close()
            except:
                fp = open("wrong.txt",'a+')
                fp.write(item)
                fp.write('\r\n')
                fp.close()
    except:
        fp = open("wrong_friend.txt",'a+')
        fp.write(search_user)
        fp.write('\r\n')
        fp.close()

fp = open("searched.txt",'a+')
for item in searched:
    fp.write(item)
    fp.write('\r\n')
fp.close()
