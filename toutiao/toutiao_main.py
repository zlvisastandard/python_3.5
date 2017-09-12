#!/usr/bin/env python
# coding:utf-8
from multiprocessing.pool import Pool

# 指定搜索的参数offset范围为[CRAWLER_GO*20,(CRAWLER_END+1)*20]
from toutiao.toutiao_crawler import main

CRAWLER_GO = 1
CRAWLER_END = 50


# 搜索关键字，可以改变

# 开启多线程
if __name__ == '__main__':
    pool = Pool()
    group = [x * 20 for x in range(CRAWLER_GO, CRAWLER_END + 1)]
    pool.map(main, group)
    pool.close()
    pool.join()
