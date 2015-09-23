# -*- coding: utf-8 -*-
# friend parser

from bs4 import BeautifulSoup


class FollowParser2(object): # the origin
    def __init__(self):
        self.pro = {
        'username':'',
        'id':'',
        'sex':'',
        'follow':'',
        'fans':'',
        'blog_num':'',
        'address':'',
        'desc':''
        }

    def _init_(self):
        self.pro = {
        'username':'',
        'id':'',
        'sex':'',
        'follow':'',
        'fans':'',
        'blog_num':'',
        'address':'',
        'desc':''
        }
    
    def parse(self,friendsoup,origin=0):
        friendsouplist = friendsoup.findAll('ul',attrs = {'class':'member_ul clearfix'})
        friendlist = []
        for friend in friendsouplist:
            self._init_()
            self._parse_friend(friend,origin)
            friendlist.append(self.pro)
        return friendlist
    
    def _parse_friend(self,friendsoup,origin=0):
        self.pro['username'],self.pro['id'] = self._get_basic(friendsoup)
        self.pro['sex'] = self._get_sex(friendsoup)
        self.pro['follow'],self.pro['fans'],self.pro['blog_num'] = self._get_popular(friendsoup)
        self.pro['address'],self.pro['desc'] = self._get_info(friendsoup,origin)
        #,self.pro['same_follow'] 
        #self.pro['mutual'] = self._get_mutual(friendsoup)
        return self.pro
        
        
    def _get_basic(self,soup):
        desc = soup.find('img')
        uid = desc['usercard'][3:]
        username = desc['alt']
        return username,uid
    
    def _get_sex(self,soup):
        return ''
    
    def _get_popular(self,soup):
        return '','',''
    
    def _get_info(self,soup,origin=0):
        return '',''


    # at the homepage, you can't get specific information about people you follow.
    # their information could be updated later
  