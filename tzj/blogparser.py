# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
import bs4
from bs4 import BeautifulSoup
from downloader import Downloader

class BlogParser:
    def __init__(self,uid = '',nickname = '',imgurl = ''):
        self.uid = uid
        self.username = nickname
        self.userimg = imgurl
        self.downloader = Downloader()
        
        self.blog = {
        'uid': self.uid,  #用户的id
        'un': self.username,  #用户用户名
        'iu': self.userimg,  #用户头像URL
        'mid': '',  #消息id
        'mc': '',  #消息内容
        'nc': [],  #消息中@的用户
        'run': '',  #转发的消息的用户名
        'ruid': '',  #转发的消息的用户ID
        'rmc': '',  #转发的消息的内容
        #'pu': '',  #消息中的图片
        # deleted on 8/9
        'rrc': '',  #转发的消息的转发次数
        'rcc': '',  #转发的消息的评论次数
        'rlc': '',  #转发的消息的赞次数，14/9/2015
        'rpage': '',  #转发的消息的微博页面
        'rpt': '',  #转发的消息的发布时间
        'rc': '0',  #消息的转发次数
        'cc': '0',  #消息的评论次数
        'lc': '0',  #消息的赞次数，14/9/2015
        'lp': '0',  #消息的赞的人，15/9/2015
        'comment': [],  #消息的评论，包括评论人，被评论人和评论内容
        'repost': [],   #消息的转发的人
        'srn': '',  #消息来源
        'page': '',  #消息的微博页面
        'pt': '',  #消息的发布时间
        'feedpin': 0  #是否置顶
        }
        pass

    def init_user(self, uid='', imgurl='', nickname=''):
        '''
        用户信息的初始化
        '''
        self.uid = uid
        self.username = nickname
        self.userimg = imgurl

    def init_blog(self):
        self.blog = {
        'uid': self.uid,  #用户的id
        'un': self.username,  #用户用户名
        'iu': self.userimg,  #用户头像URL
        'mid': '',  #消息id
        'mc': '',  #消息内容
        'nc': [],  #消息中@的用户
        'run': '',  #转发的消息的用户名
        'ruid': '',  #转发的消息的用户ID
        'rmc': '',  #转发的消息的内容
        # 'pu': '',  #消息中的图片
        'rrc': '',  #转发的消息的转发次数
        'rcc': '',  #转发的消息的评论次数
        'rlc': '',  #转发的消息的赞次数，14/9/2015
        'rpage': '',  #转发的消息的微博页面
        'rpt': '',  #转发的消息的发布时间
        'rc': '0',  #消息的转发次数
        'cc': '0',  #消息的评论次数
        'lc': '0',  #消息的赞次数，14/9/2015
        'lp': '0',  #消息的赞的人，15/9/2015
        'comment': [],  #消息的评论，包括评论人，被评论人和评论内容
        'repost': [],   #消息的转发的人
        'srn': '',  #消息来源
        'page': '',  #消息的微博页面
        'pt': '',  #消息的发布时间
        'feedpin': 0  #是否置顶
        }

    def parse(self, html):
        '''
        解析给定html字符串里面的微博数据
        -----------------------------------------
        html: 给定的html字符串
        --------------------------------------
        return: blog列表
        '''
        bpos = html.find('<!--feed内容-->')
        epos = html.find('<!--翻页-->', bpos)
        bloghtml = html[bpos:epos].replace('\\/', '/') + '</div>'   # the original one was not complete
        soup = BeautifulSoup(bloghtml)
        blogsouplist = soup.find_all('div', class_ = 'WB_feed_type')
#class_='WB_cardwrap WB_feed_type S_bg2 ')
        bloglist = []
        for blogsoup in blogsouplist:
            self.init_blog()
            self._parse_blog(blogsoup)
            bloglist.append(self.blog)
        return bloglist

    def _parse_blog(self, blogsoup):
        '''
        解析一条微博文本
        ----------------------------------------
        blogsoup: 用BeautifulSoup包装的微博文本
        '''
        raise NotImplementedError()

    def _get_attr(self, soup, attr):
        '''
        获取soup对象的attr属性值
        -------------------------------
        soup: 获取属性值的soup对象
        attr: 待获取的属性值
        -------------------------------
        return: 成功则返回获取的属性值,否则返回空串
        '''
        attrvalue = ''
        '''
        if( not attr in soup):
            print "soup"
            print soup
        '''
        if soup:
            attrvalue = soup[attr]
        return attrvalue

    def _get_text(self, soup):
        '''
        获取soup对象的text
        --------------------------------
        soup: 待获取text的soup对象
        --------------------------------
        return: 获取到的text值或返回空串
        '''
        text = ''
        if soup:
            text = soup.get_text().strip()
            tag = '//'
            pos = text.find(tag)
            # modified on 8/9
            if(pos != -1):   
                text = text[:pos]
        return text

    def _parse_statistics(self, statsoup):
        '''
        获取 转发/评论/赞 数
        ---------------------------------------
        statsoup: 统计数据所在html片段的BSoup对象
        ---------------------------------------
        return: 转发数,评论数
        '''
        forwardcount = '0'
        commentcount = '0'
        likecount = '0'
        statstr = str(statsoup)
        bpos = statstr.find('转发')
        if bpos != -1:
            epos = statstr.find('<', bpos)
            forwardcount = statstr[bpos + 6:epos]
            forwardcount = forwardcount.strip()
            if(len(forwardcount)==0):
                forwardcount = '0'
        bpos = statstr.find('评论')
        if bpos != -1:
            epos = statstr.find('<', bpos)
            commentcount = statstr[bpos + 6:epos]
            commentcount = commentcount.strip()
            if(len(commentcount)==0):
                commentcount = '0'
        like_part = statsoup.find('span',attrs = {'node-type':'like_status'})
        like_num = like_part.find('em').contents
        if(not len(like_num)):
            likecount = 0
        else:
            likecount = like_num[0].strip()
        print like_num
        return forwardcount, commentcount, likecount

    def _parse_blog_from(self, fromsoup):
        '''
        获取微博的 地址/时间/来源 等信息
        --------------------------------------
        fromsoup: 包含以上信息片段的soup
        --------------------------------------
        return: 地址,时间,来源
        '''
        page = ''
        pt = ''
        srn = ''
        asoup = fromsoup.find('a', attrs={'node-type': 'feed_list_item_date'})
        if asoup:
            pt = asoup['title']
            page = "http://www.weibo.com" + asoup['href']
        srnsoup = fromsoup.find('a', attrs={'action-type': 'app_source'})
        if srnsoup:
            srn = srnsoup.get_text().strip()
        return page, pt, srn

    def _parse_at_people(self,fromsoup):
        '''
        get the people @ in this blog
        '''
        content = fromsoup.find('div',attrs = {'class':'WB_text W_f14'})
        if( '//' in content.contents[0]):
            return []  
        friendlist = content.find_all('a',attrs = {'target':'_blank','render':'ext'})
        atlist = []
        if(friendlist):
            for friend in friendlist:
                text = friend.contents[0]
                #if( friend['class'] == 'a_topic'):
                if (friend['extra-data'] == 'type=topic'):
                    if('//' in text):
                        break
                    else:
                        continue
                user_url = friend['href']
                btag = 'weibo.com/n/'
                etag = '?from=feed'
                bpos = user_url.find(btag)+len(btag)
                epos = user_url.find(etag)
                username = user_url[bpos:epos]
                url = 'http://weibo.com/aj/v6/user/newcard?ajwvr=6&name='+username+'&type=1'
                userpage = self.downloader.download(url)
                '''
                btag = "$CONFIG['oid']='"
                etag = "';"
                '''
                if(userpage.find('"code":"100001"') != -1):
                    continue
                btag = 'uid="'
                etag = '"'
                bpos = userpage.find(btag)+len(btag)
                epos = userpage[bpos:].find(etag)+bpos
                oid = int(userpage[bpos:epos])
                print "oid",oid
                atlist.append(oid)
                if('//' in text):
                    break
        return atlist

    def _parse_like(self):
        pagenum = int(self.blog['lc'])/30+1
        like_list = []
        if(int(self.blog['lc'])%30 == 0):
            pagenum = pagenum-1
        for i in range(1,pagenum+1):
            url = 'http://www.weibo.com/aj/v6/like/big?ajwvr=6&mid='+self.blog['mid']+'&page='+str(i)
            content = self.downloader.download(url)
            content = content.replace('\\/','/')
            btag = '<div'
            etag = '</div>'
            bpos = content.find(btag)
            epos = content.rfind(etag)
            content = content[bpos:epos]
            soup = BeautifulSoup(content)
            liked = soup.find_all('li')
            for item in liked:
                if(item['uid']):
                    like_list.append(item['uid'])
        return like_list


    def _parse_comment(self):
        pagenum = int(self.blog['cc'])/20+1
        if(int(self.blog['cc'])%20 == 0):
            pagenum = pagenum-1
        comment_list = []
        username = ''
        for i in range(1,pagenum+1):    # get from each page
            url = 'http://www.weibo.com/aj/v6/comment/big?ajwvr=6&id='+self.blog['mid']+'&page='+str(i)
            content = self.downloader.download(url)
            content = content.replace('\\/','/')
            btag = '<div'
            etag = '</div'
            bpos = content.find(btag)
            epos = content.rfind(etag)
            content = content[bpos:epos]
            soup = BeautifulSoup(content)
            comment = soup.find_all('div',attrs={'class':'list_li S_line1 clearfix'})
            # get from each comment
            for item in comment:
                '''
                if(item.find('a',attrs = {'extra-data':'type=atname'})):
                    user = item.find('div', attrs ={'class':'WB_text'})
                    user_res = user.find('a',attrs={'target':'_blank'})
                    user_at = user.find('a',attrs={'extra-data':'type=atname'})
                    username = user_at['usercard'][5:]

                    user0 = user_res['usercard'][3:]
                    user_url = user_at['href']
                    btag = 'weibo.com/n/'
                    etag = '?from=feed&loc=at'
                    bpos = user_url.find(btag)+len(btag)
                    epos = user_url.find(etag)
                    username = user_url[bpos:epos]
                    url = 'http://weibo.com/aj/v6/user/newcard?ajwvr=6&name='+username+'&type=1'
                    userpage = self.downloader.download(url)
                    btag = 'uid="'
                    etag = '"'
                    bpos = userpage.find(btag)+len(btag)
                    epos = userpage[bpos:].find(etag)+bpos
                    user1 = userpage[bpos:epos]
                    users = [user0,user1]
                else:
                    user = item.find('div', attrs ={'class':'WB_text'})
                    user = user.find('a',attrs={'target':'_blank'})
                    username = user.contents[0]
                    user0 = user['usercard'][3:]
                    users = [user0]
                '''
                user = item.find('div', attrs ={'class':'WB_text'})
                user_con = user.contents
                user_at = 0
                user_res = user_con[1]['usercard'][3:]
                username = user_con[1].contents[0]
                con_len = len(user_con)
                for i in range(2,con_len):
                    if (user_con[i] == '//'):
                        break
                    else:
                        if(type(user_con[i]) != bs4.element.NavigableString):
                            con_dic = user_con[i].attrs
                            if('extra-data' in con_dic.keys()):
                                if(user_con[i]['extra-data'] == 'type=atname'):
                                    user_url = user_con[i]['href']
                                    btag = 'weibo.com/n/'
                                    etag = '?from=feed&loc=at'
                                    bpos = user_url.find(btag)+len(btag)
                                    epos = user_url.find(etag)
                                    username = user_url[bpos:epos]
                                    url = 'http://weibo.com/aj/v6/user/newcard?ajwvr=6&name='+username+'&type=1'
                                    username = user_con[i]['usercard'][5:]
                                    userpage = self.downloader.download(url)
                                    btag = 'uid="'
                                    etag = '"'
                                    bpos = userpage.find(btag)+len(btag)
                                    epos = userpage[bpos:].find(etag)+bpos
                                    user_at = userpage[bpos:epos]
                                    break
                        # modified because there might be some at in the comment that distort the information
                        # tested on Tangwei's weibo
                        # modified on 20/9/2015
                if(user_at):
                    users = [user_res,user_at]
                else:
                    users = [user_res]

                text = item.find('div',attrs = {'class':'WB_text'})
                comment_cont = text.get_text().strip()
                print "username_type", type(username)
                com_pos = comment_cont.find(username)
                print "username_len", len(username)
                comment_cont = comment_cont[com_pos+len(username)+1:]
                tag = '//'
                pos = comment_cont.find(tag)
                if(pos != -1):
                    comment_cont = comment_cont[:pos]


                time = item.find('div',attrs = {'class':'WB_from S_txt2'})
                time = time.contents[0]
                locol_time = datetime.datetime.now()
                if(time.find('分钟前')+time.find('今天') != -2):
                    str_time = locol_time.strftime("%Y-%m-%d")
                elif(time.find('昨天') != -1):
                    comment_time = locol_time-datetime.timedelta(days = 1)
                    str_time = comment_time.strftime("%Y-%m-%d")
                else:
                    comment_time = time.split()[0]
                    if(comment_time.find('月') != -1):
                        '''
                        print type(comment_time)
                        print "comment_time",comment_time
                        '''
                        mtag = '月'
                        dtag = '日'
                        pos1 = comment_time.find(mtag)
                        pos2 = comment_time.find(dtag)
                        '''
                        month = comment_time[:pos1]
                        day = comment_time[pos1+len(mtag):pos2]
                        print pos1
                        print pos2
                        print len(mtag)
                        '''
                        month = comment_time[:pos1]
                        day = comment_time[pos1+1:pos2]
                        str_time = '2015-'+month+'-'+day
                    else:
                        str_time = comment_time
                comment_list.append([users,comment_cont,str_time])
        return comment_list
                    



    def _parse_repost(self):
        pagenum = int(self.blog['rc'])/20+1
        if(int(self.blog['rc'])%20 == 0):
            pagenum = pagenum-1
        repost_list = []
        for i in range(1,pagenum+1):
            url = 'http://www.weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+self.blog['mid']+'&page='+str(i)
            content = self.downloader.download(url)
            content = content.replace('\\/','/')
            btag = '<div'
            etag = '</div'
            bpos = content.find(btag)
            epos = content.rfind(etag)
            content = content[bpos:epos]
            soup = BeautifulSoup(content)
            repost = soup.find_all('div',attrs = {'class':'list_li S_line1 clearfix'})
            for item in repost:
                repost_data = item.find('div',attrs = {'class':'WB_face W_fl'})
                repost_data = repost_data.find('img')
                repost_user = repost_data['usercard'][3:]
                repost_list.append(repost_user)
        return repost_list
        # only contain the users' ID number, the text together was omitted

    '''
    def output(self, blogmsg):
        print 'iu  is :' + blogmsg['iu']
        print 'un  is :' + blogmsg['un']
        print 'mid is :' + blogmsg['mid']
        print 'mc  is :' + blogmsg['mc']
        print 'nc  is :' + blogmsg['nc']
        print 'run is :' + blogmsg['run']
        print 'rmc is :' + blogmsg['rmc']
        print 'pu  is :' + blogmsg['pu']
        print 'rrc is :' + blogmsg['rrc']
        print 'rcc is :' + blogmsg['rcc']
        print 'rpt is :' + blogmsg['rpt']
        print 'rpage is :' + blogmsg['rpage'] ;
        print 'rc  is :' + blogmsg['rc']
        print 'cc  is :' + blogmsg['cc']
        print 'page is :' + blogmsg['page'] ;
        print 'pt  is :' + blogmsg['pt']
        print 'srn is :' + blogmsg['srn'] ;
        print '======================================'
    '''


if __name__ == '__main__':
    import sys, os
