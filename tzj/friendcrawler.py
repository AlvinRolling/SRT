# -*- coding: utf-8 -*-
import os
import time
import math
import logging
import urllib2
from downloader import Downloader
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
from friendparser import FriendParser

class FriendCrawler(object):
    def __init__(self,uid,origin=0):
        self.downloader = Downloader()
        self.list = []
        self.parser = FriendParser()
        self.uid = uid
        self.origin = origin
        self.friendNum = self._parse_friendnum(uid,origin)
        
        # origin==1, means it's the user itself, the html is a little different 
        
    def _parse_friendnum(self,uid,origin=0):
        '''
        count the total number of blogs
        only used at the original node
        '''
        if(origin):
            url = 'http://weibo.com/p/1005052198840781/myfollow?relate=fans'
            content = self.downloader.download(url)
            btag = '粉丝<\/span><em class="num S_txt1">'
            etag = '<\/em>'
            bpos = content.find(btag)+len(btag)
            epos = content[bpos:].find(etag)+bpos
            return int(content[bpos:epos])
        else:
            url = 'http://weibo.com/p/100505'+str(uid)+'/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans'
            content = self.downloader.download(url)
            '''
            w = open("C:/Users/hp1/Desktop/weibo_crawler/test4.txt","w")
            w.write(content)
            w.close()
            '''
            btag1 = '的粉丝<\/span>'
            btag2 = '>'
            etag = '<\/em>'
            bpos = content.find(btag1)
            if(bpos == -1):
                return 0
            epos = content[bpos+len(btag1):].find(etag)+bpos+len(btag1)
            bpos = content[:epos].rfind(btag2)+len(btag2)
            if(epos==0 or bpos == 0):
                return 0
            return int(content[bpos:epos])

    def get_url(self,uid,page,origin=0):
        if(origin):
            url = 'http://weibo.com/'+str(uid)+'/myfans?cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__103_page='+str(page)
        else:
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
        '''
        filepath = self.get_filepath(self.uid)
        if os.path.isfile(filepath):  # the friends of this user has been downloaded 
            print self.uid, u'用户的好友已下载！'
            return None
        '''
        pageNum = min(10,int((self.friendNum-1)/15)+1)
        print "Friends No:",self.friendNum
        # should be careful here
        # 10 is the maximun number of pages we could get
        for i in range(1,pageNum+1):
            html = self.downloader.download(self.get_url(self.uid,i,self.origin))
            html = html.decode('utf-8','ignore')
            new_friend = self.parse_friend(html,self.origin)
            if(new_friend):
                self.list.append(new_friend)
        return self.list
    
        
    def parse_friend(self,content,origin=0):
        btag = '<div class="W_tips tips_warn clearfix">'
        if(not origin):
            etag = '<ul class="follow_list" node-type="userListBox">'
        else:
            etag = '<ul class="follow_list">'
        bpos = content.find(btag)
        epos = content.find(etag)
        content = content[epos:bpos]
        content = self._process_html(content)
        if(len(content) == 0):
            print "Content matching failed."
            return None
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
        