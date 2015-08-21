# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import math
from bs4 import BeautifulSoup

import config
#from toolkit.downloader import Downloader, DownloadError
#from toolkit import datetimelib as dt
#from parser.commonblogparser import CommonBlogParser

from downloader import Downloader#, DownloadError
import datetimelib as dt
from commonblogparser import CommonBlogParser


class PreprocessError(Exception):
    """
    预处理过程中遇到的异常
    """

    def __init__(self, uid=''):
        self.error_msg = "Preprocess %s error in blog crawler." % uid

    def __str__(self):
        return repr(self.error_msg)


class UserNotFoundError(PreprocessError):
    """
    用户不存在
    """

    def __init__(self, uid=''):
        self.error_msg = "User %s not found." % uid

    def __str__(self):
        return repr(self.error_msg)


class BlogCrawler(object):
    def __init__(self):
        self.charset = 'utf-8'
        self.parser = CommonBlogParser()
        cookie = 'SINAGLOBAL=1741986363194.8828.1402790278112; __gads=ID=c89a3aae13e8c3fb:T=1439276319:S=ALNI_Ma4dDrxRssSQmWPGRnmbUMuXggH2g; myuid=5680912796; wvr=6; un=595463155@qq.com; YF-V5-G0=8a3c37d39afd53b5f9eb3c8fb1874eec; SUS=SID-2198840781-1440032052-GZ-s849g-460ec2d7418e98f7ba73ff0dcd5660b2; SUE=es%3Db8fb58e8d4ba85910d0316e97689dfc1%26ev%3Dv1%26es2%3D43d3a74a1a96e2740e833edf5f89531c%26rs0%3DsuKJLH8TSZ%252FcKueYVwCyEXLo1qJBX08KBoxqzd1i%252Fnl6prd08N1zoZ22dqZqxsdJcIc2lcmz8T%252F%252BiMnHemaUEyizlqtlPd%252Bn%252Fb8qTbmBGE6o4MdQW5%252FWsaW7S2Lg9fNkeD9fPjtV07YcjNWFsHm%252BLTGlUkWXd%252BMWUgOBCXcPAVM%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1440032052%26et%3D1440118452%26d%3Dc909%26i%3D60b2%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2198840781%26name%3D595463155%2540qq.com%26nick%3D%25E6%2589%2580%25E6%259C%2589%25E6%25B5%2581%25E6%25B5%25AA%25E7%259A%2584%25E7%25BB%2588%25E7%2582%25B9%26fmp%3D%26lcp%3D2012-01-18%252012%253A13%253A29; SUB=_2A2540VVkDeTxGeRP4loZ9C7Lwz2IHXVbp8GsrDV8PUNbu9BeLUL_kW9FBt7hnsnU013KTFZ-2PNhFYmjDg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56UcJIJGJ6mhRLk-T6h53C5JpX5Kzt; SUHB=03oEa-w2ygZUJX; ALF=1471568051; SSOLoginState=1440032052; _s_tentry=login.sina.com.cn; Apache=3630375503562.3906.1440032051163; ULV=1440032051224:48:18:10:3630375503562.3906.1440032051163:1439971935664; UOR=,,login.sina.com.cn; YF-Page-G0=3d55e26bde550ac7b0d32a2ad7d6fa53; WBStore=4e40f953589b7b00|undefined; YF-Ugrow-G0=4703aa1c27ac0c4bab8fc0fc5968141e'
        self.downloader = Downloader(cookie)
        # 设置页面url加载的参数
        self.uid = ''

    # =========  完成解析用户微博数据前的准备工作  ========#
    def _init_(self, url):
        """
        解析用户微博数据前的准备工作,包括:
        1. 获取当前用户的page_id
        2. 获取当前用户的微博总页数
        """
        self.http_params = {
            '_t':'0',  
            'count':'50',  
            'page':1,  
            'pagebar':'',  
            'pre_page':'0'  
        }
        content = self.downloader.download(url)
        # 判断用户是否存在
        if not self.exist(content):
            raise UserNotFoundError(url)
        # 获取用户ID
        btag = "$CONFIG['oid']='"
        etag = "';"
        bpos = content.find(btag) + len(btag)
        epos = content.find(etag, bpos)
        uid = content[bpos:epos]
        self.uid = uid
        # 获取 page_id
        self.page_id = self._parse_pageid(content)
        # 获取微博总页数
        self.pagenum = self._caculate_pagenum(content)
        # 获取pid,抓取微博所需的domain参数
        self.pid = self._parse_pid(content)
        # 获取用户头像地址和昵称
        img_url, nick_name = self._parse_userinfo(content)
        self.parser.init_user(self.uid, img_url, nick_name)
        self.url = self.get_url(uid)

    def exist(self, content):
        """
        判断当前用户是否存在
        ------------------------------
        return: 用户存在返回True,否则返回False
        """
        if content.find('<title>错误提示') != -1:
            return False
        return True

    def _parse_pageid(self, content):
        """
        解析页面的page_id
        ----------------------------------
        
        content: 待解析的网页内容
        ----------------------------------
        return: page_id, 或空
        """
        btag = "$CONFIG['page_id']='"
        etag = "'"
        page_id = ''
        if content:
            bpos = content.find(btag)
            if bpos:
                bpos += len(btag)
                epos = content.find(etag, bpos)
                page_id = content[bpos:epos]
        return page_id

    def _caculate_pagenum(self, content):
        """
        计算微博的总页数
        ------------------------------
        return: 微博页数
        """
        msgcount = self._parse_msgcount(content)
        per_pagenum = 45
        total_pagenum = msgcount / per_pagenum
        if msgcount % per_pagenum:
            total_pagenum += 1
        return total_pagenum

    def _parse_msgcount(self, content):
        """
        解析微博条数
        ---------------------------
        content: 网页文本
        ---------------------------
        return: 微博条数
        """
        if not content:
            raise PreprocessError(self.uid)
        etag1 = '>微博<\/span>'
        etag2 = '<\/strong>'
        btag = '>'
        epos = content.find(etag1)
        epos = content[:epos].rfind(etag2)
        bpos = content[:epos].rfind(btag) + len(btag)
        return int(content[bpos:epos])

    def _parse_userinfo(self, content):
        """
        解析用户的头像地址/用户昵称
        -----------------------------
        content: 网页文本
        ------------------------------
        return: (img_url, nick_name)
        """
        btag = '<div class="pf_photo"'
        etag = '<\/div>'
        bpos = content.find(btag)
        epos = content.find(etag, bpos)
        soup = BeautifulSoup(content[bpos:epos].replace('\\/', '/') + '</div>')
        img_url = soup.img['src']
        nick_name = soup.img['alt']
        return img_url, nick_name
        
    def get_filepath(self,uid):
        filepath = "C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_blog.txt"
        return filepath

    #========   解析用户的微博数据,并保存结果   =======#
    def scratch(self, uid, start_pageindex=1):
        """
        获取给定用户的所有满足条件的微博,并写入文件
        ----------------------------------------
        uid: 待抓取微博数据的用户ID
        start_pageindex: 从第几页开始抓取用户的微博数据
        """
        self._init_(self.get_url(uid))
        if os.path.isfile(self.get_filepath(uid)):  # 用户微博已下载
            print self.uid, u'用户的微博已下载！'
            return None
        if start_pageindex > self.pagenum:
            return []
        scrach_result = self._sequence_scratch(self.uid, start_pageindex, self.pagenum)
        w = open(self.get_filepath(uid),"w")
        L = len(scrach_result)
        print "length: ",L
        for i in range(0,L):
            key = scrach_result[i].keys()
            for item in key:
                w.write(item)
                w.write(": \t")
                w.write(str(scrach_result[i][item]))
                w.write('\n')
            w.write('\n')
        w.close()
        
    def _sequence_scratch(self, uid, start_pageindex, end_pageindex, direction=1):
        """
        执行顺序抓取策略,按照顺序从前往后或者从后往前抓取
        ---------------------------------------------------
        uid: 待抓取的用户ID
        start_pageindex: 起始页码
        end_pageindex: 结束页面
        direction: 抓取的方向, 1->从前往后,pageindex递增;-1->从后往前,pageindex递减
        ---------------------------------------------------
        return: blogs
        """
        blogs = []
        for pageindex in range(start_pageindex, end_pageindex + direction, direction):
            temp_blogs = self._parse_blogs(pageindex)
            print uid + ':获取第' + str(pageindex) + '页微博成功.'
            blogs.extend(temp_blogs)
            time.sleep(1)
            if not self._continue(temp_blogs, direction):
                break
        return blogs

    def _parse_blogs(self, pageindex):
        """
        获取指定微博页面的三个子页的微博内容
        -----------------------------------
        return: 该页的微博列表
        """
        blogs = []
        self.http_params['page'] = pageindex
        self.http_params['count'] = '50'
        self.http_params['pagebar'] = ''
        # 下载第一页
        self.http_params['pre_page'] = self.http_params['page'] - 1
        content = self.downloader.download(self.url, self.http_params)
        if content:
            sub_blogs = self.parser.parse(content)
            blogs.extend(sub_blogs)
        if not self._continue(blogs):
            return blogs
        # 下载第二页
        self.http_params['count'] = '15'
        self.http_params['pagebar'] = '0'
        self.http_params['pre_page'] = self.http_params['page']
        content = self.downloader.download(self.url, self.http_params)
        if content:
            sub_blogs = self.parser.parse(content)
            blogs.extend(sub_blogs)
            if not self._continue(sub_blogs):
                return blogs
        # 下载第三页
        self.http_params['count'] = '15'
        self.http_params['pagebar'] = '1'
        self.http_params['pre_page'] = self.http_params['page']
        content = self.downloader.download(self.url, self.http_params)
        if content:
            sub_blogs = self.parser.parse(content)
            blogs.extend(sub_blogs)
        return blogs

    def _continue(self, blogs, direction=1):
        """
        判断是否需要继续进行下载任务
        -----------------------------
        blogs: 待判断的博客列表,按照时间先后顺序排列
        direction: 判别的方向,1->判定最后一条微博是否比起始时间早;
            -1->判定第一条微博是否比结束时间晚;
        ------------------------------
        return: 继续返回True,否则返回False
        """
        is_continue = True
        if blogs:
            if (direction == -1 and dt.compare(blogs[0]['pt'], config.end_time) > 0) or \
                    (direction == 1 and dt.compare(blogs[-1]['pt'], config.begin_time) < 0):
                is_continue = False
        return is_continue

    def get_url(self,uid):
        """
        获取下载的网页地址
        """
        url = 'http://weibo.com/' + str(uid) + '?from=otherprofile&'
        return url

    def _parse_pid(self, content):
        btag = "$CONFIG['pid']='"
        etag = "'"
        pid = ''
        if content:
            bpos = content.find(btag)
            if bpos:
                bpos += len(btag)
                epos = content.find(etag, bpos)
                pid = content[bpos:epos]
        return pid


if __name__ == '__main__':
    '''
    from toolkit.accountlib import AccountManager
    # 进行模拟登录
    account_assistant = AccountManager()
    try:
        account_assistant.init()
        account_assistant.login()
        print '模拟登录成功!'
    except Exception, e:
        print '模拟登录失败!'
        print e
        exit()
    '''
    blogcrawler = BlogCrawler()
    print blogcrawler.scratch('2034424692')