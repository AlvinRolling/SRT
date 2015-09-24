# -*- coding: utf-8 -*-
from blogcrawler import BlogCrawler

bc = BlogCrawler()
uid = '3893160417'

bc._init_(bc.get_url(uid))
t = bc._sequence_scratch(uid,1,1)