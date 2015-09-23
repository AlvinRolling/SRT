# -*- coding: utf-8 -*-
# Follow Parser
# FollowParser1 for normal nodes
# FollowParser2 for the original node

from bs4 import BeautifulSoup


class FollowParser1(object):    # not the origin
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
        friendsouplist = friendsoup.findAll('li',attrs = {'class':'follow_item S_line2'})
        friendlist = []
        for friend in friendsouplist:
            self._init_()
            check = self._parse_friend(friend,origin)
            if(check):
                friendlist.append(self.pro)
        return friendlist
    
    def _parse_friend(self,friendsoup,origin=0):
        self.pro['username'],self.pro['id'] = self._get_basic(friendsoup)
        if(len(self.pro['username']) == 0):
            return None
        self.pro['sex'] = self._get_sex(friendsoup)
        self.pro['follow'],self.pro['fans'],self.pro['blog_num'] = self._get_popular(friendsoup)
        self.pro['address'],self.pro['desc'] = self._get_info(friendsoup,origin)
        #,self.pro['same_follow'] 
        #self.pro['mutual'] = self._get_mutual(friendsoup)
        return self.pro
        
        
    def _get_basic(self,soup):
        desc = soup.find('img')
        try:
            uid = desc['usercard'][3:]
        except KeyError:
            return '',''
        username = desc['alt']
        return username,uid
    
    def _get_sex(self,soup):
        content = soup.find('i')
        sex = content['class'][1]
        sex = sex[5:]
        return sex
    
    def _get_popular(self,soup):
        relation = soup.findAll('span',attrs={'class':'conn_type'})
        follow = relation[0].find('a').contents[0]
        fans = relation[1].find('a').contents[0]
        blog_num = relation[2].find('a').contents[0]
        return follow,fans,blog_num
    
    def _get_info(self,soup,origin=0):
        add = soup.find('div',attrs = {'class':'info_add'})
        if(add):
            add = add.find('span')
            address = add.contents[0]
        else:
            address = ''
            
        intro = soup.find('div',attrs={'class':'info_intro'})
        if(intro):
            introduction = intro.find('span').contents[0]
        else:
            introduction = ''
            
        return address,introduction

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
        friendsouplist = friendsoup.findAll('li',attrs = {'class':'member_li S_bg1'})
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
        return '0','0','0'
    
    def _get_info(self,soup,origin=0):
        return '',''


    # at the homepage, you can't get specific information about people you follow.
    # their information could be updated later
  