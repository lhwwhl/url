#!/usr/bin/env python
# coding:utf-8

from bs4 import BeautifulSoup as bs
import requests
#import sys  
import jieba
import pandas as pd
import re
import string

resp = requests.get('http://movie.douban.com/nowplaying/beijing/')
html_data = resp.text
#print resp.encoding
#print html_data
soup = bs(html_data, 'html.parser')
nowplaying_movie = soup.find_all('div', id='nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
#print nowplaying_movie_list
nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)

requrl = 'http://movie.douban.com/subject/' + nowplaying_list[0]['id'] + '/comments' + '?' + 'start=0' +'&limit=20'
pinglun = requests.get(requrl)
pinglun_data = pinglun.text
soup_comm = bs(pinglun_data, 'html.parser')
comment_div_list = soup_comm.find_all('div', class_='comment')

def getcomment(comm):
    eachcommentlist = []
    for item in comm:
        if item.find_all('p')[0].string is not None:
            #print type(item.find_all('p')[0].string)
            eachcommentlist.append(item.find_all('p')[0].string)
            #print eachcommentlist
    print type(eachcommentlist)
    return eachcommentlist

pinglunneirong = ''

neirong = getcomment(comment_div_list)
commentList = []
commentList.append(neirong)
for k in range(len(commentList)):
    print type((str(commentList[k])).strip())
    pinglunneirong = pinglunneirong + (str(commentList[k])).strip()
#print pinglunneirong 

#line = '今天，非常开心。'
#print type(line)
#pattern = re.compile(r'[\u4e00-\u9fa5]+')
#filterdata = re.findall(pattern, line)
#print filterdata
#cleaned_comments = " ".join(filterdata)
#print cleaned_comments

#segment = jieba.lcut('我今天来到了好未来')
#print ", ".join(segment)
#words_df = pd.DataFrame({'segment':segment})
#words_df.head()
