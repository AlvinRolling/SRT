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
        self.downloader = Downloader()
        self.list = []
        self.parser = FriendParser()
        self.uid = uid
        self.origin = origin
        
        # origin==1, means it's the user itself, the html is a little different 
        
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

    def get_filepath(self,uid):
        filepath = "C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_friends.txt"
        return filepath
        
    def scratch(self):
        filepath = self.get_filepath(self.uid)
        if os.path.isfile(filepath):  # the friends of this user has been downloaded 
            print self.uid, u'用户的好友已下载！'
            return None
        for i in range(1,11):
            html = self.downloader.download(self.get_url(self.uid,i))
            html = html.decode('utf-8','ignore')
            new_friend = self.parse_friend(html,self.origin)
            self.list.append(new_friend)
        return self.list
    
        
    def parse_friend(self,content,origin=0):
        btag = '<div class="W_tips tips_warn clearfix">'
        w = open("C:/Users/hp1/Desktop/weibo_crawler/test.txt","w")
        w.write(content)
        w.close()
        if(not origin):
            etag = '<ul class="follow_list" node-type="userListBox">'
        else:
            etag = '<ul class="follow_list">'
        bpos = content.find(btag)
        epos = content.find(etag)
        content = content[epos:bpos]
        content = self._process_html(content)
        if(len(content) == 0):
            print "wrong"
        soup = BeautifulSoup(content)
        return self.parser.parse(soup,self.origin)
            
            
        
if __name__ == '__main__':
    uid = 2198840781
    fc = FriendCrawler(uid,1)
    result = fc.scratch()
    print result
    l = len(result)
    w = open("C:/Users/hp1/Desktop/weibo_crawler/2198840781_friends.txt","w")
    id_only = open("C:/Users/hp1/Desktop/weibo_crawler/2198840781_friends_id.txt","w")
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
        