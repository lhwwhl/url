#!/usr/bin/env python3.5
#coding:utf-8

import warnings
warnings.filterwarnings("ignore")
import jieba    #分词包
import numpy    #numpy计算包
import codecs   #codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode
import re
import pandas as pd  
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
#%matplotlib inline

import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud#词云包

#分析网页函数
def getNowPlayingMovie_list():  
    resp = requests.get('https://movie.douban.com/nowplaying/hangzhou/') 
    resp.encoding = 'utf-8'
    html_data = resp.text    
    soup = bs(html_data, 'html.parser')    
    nowplaying_movie = soup.find_all('div', id='nowplaying')        
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')    
    nowplaying_list = []    
    for item in nowplaying_movie_list:        
        nowplaying_dict = {}        
        nowplaying_dict['id'] = item['data-subject']      
        for tag_img_item in item.find_all('img'):            
            nowplaying_dict['name'] = tag_img_item['alt']            
            nowplaying_list.append(nowplaying_dict)    
            return nowplaying_list

#爬取评论函数
def getCommentsById(movieId, pageNum):
    eachCommentList = [];
    if pageNum>0:
        start = (pageNum-1) * 20
    else:
        return False
    requrl = 'https://movie.douban.com/subject/' + movieId + '/comments' +'?' +'start=' + str(start) + '&limit=20'
    #print(requrl)
    resp = requests.get(requrl)
    resp.encoding = 'utf-8'
    html_data = resp.text
    #print 'type(html_data):',type(html_data)
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')
    for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:    
            #print 'item:', item.find_all('p')[0].string 
            eachCommentList.append(item.find_all('p')[0].string)
    return eachCommentList
def main():
    #循环获取第一个电影的前10页评论
    commentList = []
    NowPlayingMovie_list = getNowPlayingMovie_list()
    #for i in range(10):    
    #    num = i + 1
    commentList_temp = getCommentsById(NowPlayingMovie_list[0]['id'], 1)
    commentList.append(commentList_temp)

    #将列表中的数据转换为字符串
    comments = ''
    #print 'type(comments):', type(comments)
    for k in range(len(commentList)):
        #print type((str(commentList[k])).strip()),(str(commentList[k])).strip()
        comments = comments + (str(commentList[k])).strip()
    print('comments=', comments)
    #使用正则表达式去除标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    print('filterdata:',filterdata)
    cleaned_comments = ''.join(filterdata)
    print(cleaned_comments)
    #使用结巴分词进行中文分词
    segment = jieba.lcut(cleaned_comments)
    words_df=pd.DataFrame({'segment':segment})
    ##去掉停用词
    stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
    ##统计词频
    words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    ##用词云进行显示
    wordcloud=WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80)
    word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
    word_frequence_list = []
    for key in word_frequence:
        temp = (key,word_frequence[key])
        word_frequence_list.append(temp)
    wordcloud=wordcloud.fit_words(word_frequence_list)
    plt.imshow(wordcloud)
#主函数
main()
