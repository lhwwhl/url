#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
import cookielib
 
filename = 'cookie.txt'

cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
data = urllib.urlencode({'Username':'刘姐','Pwd':'000000'})

loginUrl = 'http://eco.mantu.co/mgr_login.html'
geturl = loginUrl + "?" + data

result = opener.open(geturl)
print result.read()

cookie.save(ignore_discard=True, ignore_expires=True)

gradeUrl = 'http://eco.mantu.co/mgr_course_school.html'

result = opener.open(gradeUrl)
print result.read()
