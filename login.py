#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2

values = {"Username":"乔岩","Pwd":"000000"}
data = urllib.urlencode(values)
url = "http://eco.mantu.co/mgr_login.html"
geturl = url + "?" + data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()
