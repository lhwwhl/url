#!/usr/bin/env python
# coding=utf-8

import requests

headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

}
values = {"Username":"乔岩","Pwd":"000000"}
html = requests.get("http://eco.mantu.co/mgr_login.html", params = values)
print html.url
html.encoding = 'utf-8'
grade = requests.get("http://eco.mantu.co/mgr_course_school.html", headers=headers)
grade.encoding = 'utf-8'
print grade.text
