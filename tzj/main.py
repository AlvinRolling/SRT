# -*- coding: utf-8 -*-

import downloader
from account import Account
import datetimelib
import filelib
import time
import blogparser
import commonblogparser
import os
import blogcrawler
from friendcrawler import FriendCrawler
from blogcrawler import BlogCrawler
from followcrawler import FollowCrawler
import config

from writefile import WriteFile

def read_users(filename):
    #filename = "to_be_searched.txt"
    f = open(filename,"r")
    
    user_list = []
    while True:
        line = f.readline()
        if line:
            user_list.append(line.strip())
        else:
            break
    return user_list

f = open("account.txt","r")
account_list = []
while(True):
    line = f.readline()
    if(line):
        temp = line.split()
        account_list.append(temp)
    else:
        break
f.close()
user_rank = 0

t1 = time.time()
test = Account()
while(True):
    if(test.login(account_list[0][0],account_list[0][1])):
        break
init_time = time.time()
#to_be_searched = [1995234631]  
#to_be_searched = [5102872939]
to_be_searched = read_users("to_be_searched.txt")
searched = read_users("searched.txt")
#to_be_searched = [3737537255]
searched = []
blogcrawler = BlogCrawler()
writefile = WriteFile()

f = open("count.txt","r")
line = f.readline()
line = line.strip()
sumcount = int(line)

while(len(to_be_searched) > 0):
    t2 = time.time()
    all_time = t2-init_time
    # if(all_time>(3600*3)):
    #     break
    delta_t = t2-t1
    print "user_time: ",delta_t
    print "all_time: ", all_time
    if(delta_t> 300):
        # refresh the cookie every hour
        t1 = time.time()
        user_rank = (user_rank+1)%4
        while(True):
            if(test.login(account_list[user_rank][0],account_list[user_rank][1])):
                break
    sumcount = sumcount+1
    print "User Count: ",sumcount
    if(sumcount > 3000): # input the number of users we need 
        break
    uid = to_be_searched.pop(0)
    if(uid == 2198840781):
        origin = 1  # the homepage of fans is a little different from the others'
    else:
        origin = 0  
    #try:
    if( not os.path.exists(str(uid))):
        os.mkdir(str(uid))
    try:
        blog = blogcrawler.scratch(str(uid))    # get users blogs 
        if(len(blog)>2000):
            continue
        # modified on 9/11
        writefile.write_blog(uid,blog)          # write them in the file    
        print "Blogs of "+str(uid)+" were recorded."
        friendcrawler = FriendCrawler(uid,origin)   # get users friends
        friends = friendcrawler.scratch()
        writefile.write_fans(uid,friends)     # write friends info
        print "Fans of "+str(uid)+" were recorded."
        followcrawler = FollowCrawler(uid,origin)
        follow = followcrawler.scratch()
        writefile.write_follows(uid,follow)
        print "Follows of "+str(uid)+" were recorded."
        fopen_id = open(str(uid)+"/"+str(uid)+"_fans_id.txt","r")       
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

        #fopen_id = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_follows_id.txt","r")
        fopen_id = open(str(uid)+"/"+str(uid)+"_follows_id.txt","r")        
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
        #f = open("C:/Users/hp1/Desktop/weibo_crawler/searched.txt","a+")
        f = open("searched.txt","a+")
        f.write(str(uid))
        f.write('\n')
        f.close()
        
        #f = open("C:/Users/hp1/Desktop/weibo_crawler/to_be_searched.txt","w")
        f = open("to_be_searched.txt","w")
        for item in to_be_searched:
            f.write(str(item))
            f.write('\n')
        f.close()

        f = open("count.txt","w")
        f.write(str(sumcount))
        f.close()
    except:
        f = open("wrong.txt","a+")
        f.write(str(uid))
        f.write('\n')
        f.close()
        



