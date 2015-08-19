
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

test = Account()
test.login()
'''
url = 'http://weibo.com/u/2697416452'
result =  test.getData(url)
print result
'''

FC = FriendCrawler()
friends = FC.get_friends(2034424692)
print friends
WF = WriteFile()
WF.write_friend(2034424692,friends)