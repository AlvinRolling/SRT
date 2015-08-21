# -*- coding: utf-8 -*-
# friend parser

from bs4 import BeautifulSoup


class FriendParser(object):
    def __init__(self):
        self.pro = {
        'username':'',
        'id':'',
        'sex':'',
        'follow':'',
        'fans':'',
        'blog_num':'',
        'address':'',
        'desc':'',
        'same_follow':'',
        'mutual':''
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
        'desc':'',
        'same_follow':'',
        'mutual':''
        }
    
    def parse(self,friendsoup,origin=0):
        friendsouplist = friendsoup.findAll('li',attrs = {'class':'follow_item S_line2'})
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
        self.pro['address'],self.pro['desc'],self.pro['same_follow'] = self._get_info(friendsoup,origin)
        self.pro['mutual'] = self._get_mutual(friendsoup)
        return self.pro
        
        
    def _get_basic(self,soup):
        desc = soup.find('img')
        print "desc: ",desc
        uid = desc['usercard'][3:]
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
            if(origin):
                etag = '</em>'
                btag = '</div>'
                add = str(add)
                epos = add.find(etag)
                bpos = add.find(btag)
                address = add[epos+len(etag):bpos]
            else:
                add = add.find('span')
                address = add.contents[0]
        else:
            address = ''
            
        intro = soup.find('div',attrs={'class':'info_intro'})
        if(intro):
            introduction = intro.find('span').contents[0]
        else:
            introduction = ''
            
        rela = soup.find('div',attrs={'class':'info_relation'})
        if(rela):
            etag = '等'
            btag = '人'
            rela = str(rela)
            epos = rela.find(etag)
            bpos = rela.find(btag)
            relation = rela[epos+len(etag):bpos]
        else:
            relation = ''
        return address,introduction,relation
        
    def _get_mutual(self,soup):  
        mutual = soup.find('em',attrs={'class':'ficon_add'})
        # 'ficon_add', then not mutual
        if(mutual):
            return '0'
        else:
            return '1'
    
        
        
    
        
        