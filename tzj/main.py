
import downloader
from account import Account
import datetimelib
import filelib

import blogparser
import commonblogparser

import blogcrawler
from friendcrawler import FriendCrawler
from blogcrawler import BlogCrawler
import config

from writefile import WriteFile

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
'''

to_be_searched = [2198840781]
searched = []
blogcrawler = BlogCrawler()
writefile = WriteFile()


while(len(to_be_searched) > 0):
    uid = to_be_searched.pop()
    if(uid == 2198840781):
        origin = 1
    else:
        origin = 0  
    #try:
    blog = blogcrawler.scratch(str(uid))
    writefile.write_blog(uid,blog)
    friendcrawler = FriendCrawler(uid,origin)
    friends = friendcrawler.scratch()
    writefile.write_friend(uid,friends)
    #try:
    fopen_id = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_friends_id.txt","r")        
    # read friends from the file saved above
    
    while True:    
        new_friend = fopen_id.readline()
        if(new_friend):        
            new_friend = int(new_friend.strip())
            if(new_friend in searched):
                continue
            else:
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
        
        
        




