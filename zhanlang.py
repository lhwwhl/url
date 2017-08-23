#!/usr/bin/env python
# coding:utf-8

#from __future__ import print_function
from bs4 import BeautifulSoup as bs
import requests
import sys  
import jieba
import pandas as pd
import re
import string

def getNowPlayMovie_list():
    resp = requests.get('http://movie.douban.com/nowplaying/beijing/')
    html_data = resp.text
    #print resp.encoding
    #print html_data
    soup = bs(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    #print nowplaying_movie_listnowplaying_list = []
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
            return nowplaying_list

def getCommentsById(movieId, pageNum):
    eachCommentList = [];
    requrl = 'http://movie.douban.com/subject/' + movieId + '/comments' + '?' + 'start=0' +'&limit=20'
    resp = requests.get(requrl)
    html_data = resp.text
    #print 'type html_data', type(html_data)
    soup = bs(html_data, 'html.parser')
    comment_div_list = soup.find_all('div', class_='comment')
    print comment_div_list
    for item in comment_div_list:
        if item.find_all('p')[0].string is not None:
            print 'item', item.find_all('p')[0].string
            eachCommentList.append(item.find_all('p')[0].string)
            #print eachCommentList
    return eachCommentList
def main():
    commentList = []
    NowPlayMovie_list = getNowPlayMovie_list()
    commentList_temp = getCommentsById(NowPlayMovie_list[0]['id'], 1)
    commentList.append(commentList_temp)
    comments = ''
    #print len(commentList)
    for k in range(len(commentList)):
        comments = comments + (str(commentList[k])).strip()
    #print 'comments:', comments
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    #print filterdata
    cleaned_comments = ''.join(filterdata)
    #print cleaned_comments
    #segment = jieba.lcut('我今天来到了好未来')
    #print ", ".join(segment)
    #words_df = pd.DataFrame({'segment':segment})
    #words_df.head()
main()
