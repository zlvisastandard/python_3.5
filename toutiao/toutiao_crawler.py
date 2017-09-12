#!/usr/bin/env python
# coding:utf-8
import json
from urllib.parse import urlencode

import pymysql
from bs4 import BeautifulSoup
import requests
from requests import RequestException

# 需要指定编码集,不然会出异常
db = pymysql.connect("localhost", "root", "1234", "ssm", use_unicode=True, charset='utf8')
cursor = db.cursor()
KEYWORD = '程序员'


# 获取索引页
def get_index_page(offset, keyword):
    query_data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,  # 每次返回 20 篇文章
        'cur_tab': 1
    }
    params = urlencode(query_data)
    # 头条收索api基础入口
    base_url = 'http://www.toutiao.com/search_content/'
    url = base_url + '?' + params
    # print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        return None
    except RequestException:
        print("页面索引出错,url")
        return None


# 解析数据,获取想要的数据
def parse_index_page(html):
    params = []
    data = json.loads(html)
    datas = data['data']
    for item in datas:
        if 'title' in item:  # 文章标题
            title = item['title']
        if 'source' in item:  # 资源归属
            source = item['source']
        if 'article_url' in item:  # 资源链接
            url = item['article_url']
        if 'share_url' in item:  # 分享链接,可作资源链接用
            share_url = item['share_url']
        if 'keywords' in item:  # 所属关键词
            keyword = item['keywords']
        if 'comment_count' in item:  # 评论数
            countgood = item['comment_count']
        if 'has_video' in item:  # 是否是视频链接
            has_video = item['has_video']
            params.append([title, source, url, share_url, keyword, countgood, has_video])
    return params


# 储存至数据库
def save_data(params):
    try:
        sql = 'INSERT INTO toutiao_python VALUES (%s,%s,%s,%s,%s,%s,%s)'
        # 批量插入数据库
        cursor.executemany(sql, params)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


# 获取详情页(暂时未用)
def get_detail_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("页面详情出错", url)
        return None


# 解析详情页面(解析具体页面,暂时未用)
def parse_detail_page(html, url):
    param = []
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    return param


def main(offset):
    html = get_index_page(offset, KEYWORD)
    params = parse_index_page(html)
    # 储存到数据库
    save_data(params)

    # for param in params:
    #     html = get_detail_page(param[2])
    # res = parse_detail_page(html, param[2])
    # print(param)
