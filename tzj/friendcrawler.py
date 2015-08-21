# -*- coding: utf-8 -*-
import os
import time
import math
import logging
import urllib2
from downloader import Downloader
from bs4 import BeautifulSoup
from friendparser import FriendParser

class FriendCrawler(object):
    def __init__(self,uid,origin=0):
        cookie = 'SINAGLOBAL=1741986363194.8828.1402790278112; __gads=ID=c89a3aae13e8c3fb:T=1439276319:S=ALNI_Ma4dDrxRssSQmWPGRnmbUMuXggH2g; myuid=5680912796; UOR=,,login.sina.com.cn; wvr=6; login_sid_t=6b9baf6074cea450f1886b41d24ab295; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; SUS=SID-2198840781-1439971944-GZ-ovnsg-f8508ff3ee9d4ef6f9c107b0f21260b2; SUE=es%3D48a4dbc42fba0401ab3bbe0e5540b3f2%26ev%3Dv1%26es2%3Dd61e05f524a6f11dddf48525e8728c98%26rs0%3DBqFwcvHknPaixpdIGZOl2zyVdsa7efAqqN3v%252BZTGXfQxVwRMiGZmrs%252B8spxkZW44QI4cTuu0h0LGtT8ieUj%252BtVJKxfwC22mROkWYK%252BeUcKCZXvFLRRrmuhJ9kH5WqyLH%252BmG9UICFEKmbaO1kSzUQ5H7%252FMHw%252BirBYRaseNgeQ7GM%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1439971944%26et%3D1440058344%26d%3Dc909%26i%3D60b2%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2198840781%26name%3D595463155%2540qq.com%26nick%3D%25E6%2589%2580%25E6%259C%2589%25E6%25B5%2581%25E6%25B5%25AA%25E7%259A%2584%25E7%25BB%2588%25E7%2582%25B9%26fmp%3D%26lcp%3D2012-01-18%252012%253A13%253A29; SUB=_2A2540Eo4DeTxGeRP4loZ9C7Lwz2IHXVbpDzwrDV8PUNbuNBeLVSgkW80HgvKH2Fo-Br9KDZ3dklqqwxnFA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56UcJIJGJ6mhRLk-T6h53C5JpX5K2t; SUHB=04WvZscwY1peQm; ALF=1471507942; SSOLoginState=1439971944; un=595463155@qq.com; _s_tentry=passport.weibo.com; Apache=4324354231.357574.1439971935651; ULV=1439971935664:47:17:9:4324354231.357574.1439971935651:1439963666739; YF-Page-G0=140ad66ad7317901fc818d7fd7743564; YF-V5-G0=f59276155f879836eb028d7dcd01d03c'
        self.downloader = Downloader()
        self.list = []
        self.parser = FriendParser()
        self.uid = uid
        self.origin = origin
        
    def get_url(self,uid,page):
        url = 'http://weibo.com/p/100505'+str(uid)+'/follow?relate=fans&page='+str(page)
        print "url: ",url
        return url
    # get the friends url, could only get 10 pages now
    
    def _process_html(self, content):
        """
        对下载的网页进行预处理,主要是替换\/为/
        """
        if content:
            return content.replace('\\/', '/')
        return ''
    '''
    def get_friends(self,uid):
        friend_list = []
        for i in range(1,11):
            html_data = self.downloader.download(self.get_url(uid,i))
            html_data = self._process_html(html_data)
            w = open("C:/Users/hp1/Desktop/weibo_crawler/processed.txt","w")
            w.write(html_data.decode('utf-8','ignore'))
            w.close()
            if html_data is not None:
                try:
                    soup = BeautifulSoup(html_data.decode('utf-8','ignore'))
                    print "soup: "
                    print soup
                    w = open("C:/Users/hp1/Desktop/weibo_crawler/test.txt","w")
                    w.write(html_data.decode('utf-8','ignore'))
                    w.close()
                    friend_html_list = soup.findAll('li',attrs={'class':'follow_item S_line2'})
                    #friend_html_list = soup.findAll('ul', attrs={'class':'follow_list'})
                    print "friend_html_list"
                    print friend_html_list
                    for friend_html in friend_html_list:
                        info_connect = friend_html.find('dt',attrs={'class':'mod_pic'})
                        if info_connect is None:continue
                        if info_connect.find('img') is None:
                            continue
                        else:           
                            info = info_connect.find('img')
                            friend = []
                            friend.append(info['usercard'][3:]) # it has the format "id=*****"
                            friend.append(info['alt'])          # username
                        friend_list.append(friend)
                except Exception,e:
                    logging.exception("获取好友列表异常:" + str(uid) + str(e))
        return friend_list
        '''
    
    def scratch(self):
        for i in range(1,11):
            html = self.downloader.download(self.get_url(self.uid,i))
            html = html.decode('utf-8','ignore')
            new_friend = self.parse_friend(html)
            self.list.append(new_friend)
        return self.list
    
        
    def parse_friend(self,content):
        btag = '<div class="W_tips tips_warn clearfix">'
        etag = '<ul class="follow_list" node-type="userListBox">'
        bpos = content.find(btag)
        epos = content.find(etag)
        content = content[epos:bpos]
        content = self._process_html(content)
        if(len(content) == 0):
            print "wrong"
        soup = BeautifulSoup(content)
        return self.parser.parse(soup,self.origin)
            
            
        
if __name__ == '__main__':
    uid = 5200197732
    fc = FriendCrawler(uid)
    result = fc.scratch()
    print result
    l = len(result)
    w = open("C:/Users/hp1/Desktop/weibo_crawler/5200197732_friends.txt","w")
    id_only = open("C:/Users/hp1/Desktop/weibo_crawler/5200197732_friends_id.txt","w")
    for i in range(0,l):
        if(len(result[i]) > 0):
            m = len(result[i])
            for j in range(0,m):
                key = result[i][j].keys()
                for item in key:
                    w.write(item)
                    w.write(": \t")
                    w.write(str(result[i][j][item]))
                    w.write('\n')
                w.write('\n')
                id_only.write(str(result[i][j]['id']))
                id_only.write('\n')
    w.close()
    id_only.close()
        