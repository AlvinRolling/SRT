# -*- coding: utf-8 -*-

import downloader
from account import Account
import datetimelib
import filelib

import blogparser
import commonblogparser

import blogcrawler
from friendcrawler import FriendCrawler
from blogcrawler import BlogCrawler
from followcrawler import FollowCrawler
import config

from writefile import WriteFile

test = Account()
while(True):
    if(test.login()):
        break

to_be_searched = [1995234631]   # my uid
searched = []
blogcrawler = BlogCrawler()
writefile = WriteFile()

sumcount = 0;
while(len(to_be_searched) > 0):
    sumcount = sumcount+1
    if(sumcount > 3000): # input the number of users we need 
        break
    uid = to_be_searched.pop(0)
    if(uid == 2198840781):
        origin = 1  # the homepage of fans is a little different from the others'
    else:
        origin = 0  
    #try:
    blog = blogcrawler.scratch(str(uid))    # get users blogs 
    writefile.write_blog(uid,blog)          # write them in the file    
    friendcrawler = FriendCrawler(uid,origin)   # get users friends
    friends = friendcrawler.scratch()
    writefile.write_fans(uid,friends)     # write friends info
    print "Fans of "+str(uid)+" were recorded."
    followcrawler = FollowCrawler(uid,origin)
    follow = followcrawler.scratch()
    writefile.write_follows(uid,follow)
    print "Follows of "+str(uid)+" were recorded."
    
    #try:
    fopen_id = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_fans_id.txt","r")        
    # read friends from the file saved above
    
    while True:    
        new_friend = fopen_id.readline()
        if(new_friend):       
            new_friend = new_friend.split()
            new_friend = new_friend[0]
            if(new_friend in searched):
                continue
            else:
                if(new_friend not in to_be_searched):
                    to_be_searched.append(new_friend)
        else:
            break
    fopen_id.close()

    fopen_id = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_follows_id.txt","r")        
    # read friends from the file saved above
    
    while True:    
        new_friend = fopen_id.readline()
        if(new_friend):
            new_friend = new_friend.split()
            new_friend = new_friend[0]
            if(new_friend in searched):
                continue
            else:
                if(new_friend not in to_be_searched):
                    to_be_searched.append(new_friend)
        else:
            break
    fopen_id.close()
#except:
    #print "Open File Error! "
    searched.append(uid)
    f = open("C:/Users/hp1/Desktop/weibo_crawler/searched.txt","a+")
    f.write(str(uid))
    f.write('\n')
    f.close()
    
    f = open("C:/Users/hp1/Desktop/weibo_crawler/to_be_searched.txt","w")
    for item in to_be_searched:
        f.write(str(item))
        f.write('\n')
    f.close()
#except:
'''
    f = open("C:/Users/hp1/Desktop/weibo_crawler/wrong.txt","a+")
    f.write(str(uid))
    f.write('\n')
    f.close()
'''
        



