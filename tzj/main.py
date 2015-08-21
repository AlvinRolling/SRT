
import downloader
from account import Account
import datetimelib
import filelib

import blogparser
import commonblogparser

import blogcrawler
from friendcrawler import FriendCrawler
import config

from writefile import WriteFile
'''
test = Account()
test.login()
'''
r = open("C:/Users/hp1/Desktop/weibo_crawler/5200197732_friends_id.txt","r")
friend = []
while True:    
    new_friend = r.readline()
    if(new_friend):        
        friend.append(new_friend[:-1])
    else:
        break
r.close()
print friend

for item in friend:
    fc = FriendCrawler(item)
    result = fc.scratch()
    l = len(result)
    w = open("C:/Users/hp1/Desktop/weibo_crawler/"+item+"_friends.txt","w")
    id_only = open("C:/Users/hp1/Desktop/weibo_crawler/"+item+"_friends_id.txt","w")
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