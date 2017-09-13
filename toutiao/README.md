# 用python3.5逛看今日头条 #
---
#####环境:

1. win10 64位
2. python3.5.2
#####相关库
1. urllib
2. pymysql
3. json

#####爬文章入口
baseurl : http://www.toutiao.com/search_content


![](http://ww2.sinaimg.cn/crop.0.0.487.273.1000.562/005va6Hcgw1f7dvchhi04j30dj0a5wfj.jpg)

- (ps:图片来自网络)


接触python,发现python真是一门让人上瘾的语言,简单好用效率高.
不多说,直接看要做什么吧.每天看头条也是一种乐趣,当想看同一类型的头条新闻时,可以直接搜索关键字,突然间对这个搜索接口感兴趣了,为什么不把这些搜到的文章存下来然后想什么时候看就什么时候看呢?
打开头条搜索F12看看它的网络请求.
![](https://i.imgur.com/chpddT3.png)

####参数
offset=40&format=json&keyword=%E7%A8%8B%E5%BA%8F%E5%91%98&autoload=true&count=20&cur_tab=1


用代码构造参数,模拟请求
    
	#构造请求参数,模拟请求
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
    # 头条搜索api基础入口
    base_url = 'http://www.toutiao.com/search_content/'
    url = base_url + '?' + params
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
			#print(response.text)
            return response.text
        return None
    except RequestException:
        print("页面索引出错,url")
        return None

用print看看返回的结果是啥,分析请求结果(ps:每次写爬虫的时候总是觉得分析这个请求结果是最费时间的,但有时最关键的,每次还要对着页面去查这些字段的意义)

![](https://i.imgur.com/j4hBUH4.png)

找到一些想要要的信息,关键是title,article_url


    # 解析数据,获取想要的数据
	def parse_index_page(html):
    params = []
    data = json.loads(html)
    datas = data['data']
    for item in datas:
        if 'title' in item:#文章标题
            title = item['title']
        if 'source' in item:#资源归属
            source = item['source']
        if 'article_url' in item:#资源链接
            url = item['article_url']
        if 'share_url' in item:#分享链接,可作资源链接用
            share_url = item['share_url']
        if 'keywords' in item:#所属关键词
            keyword = item['keywords']
        if 'comment_count' in item:#评论数
            countgood = item['comment_count']
        if 'has_video' in item:#是否是视频链接
            has_video = item['has_video']
            params.append([title, source, url, share_url, keyword, countgood, has_video])
    return params

已经拿到一些数据了,要对数据进行储存
使用的pymysql库进行MySQL数据库操作
    
	# 需要指定编码集,不然会出异常!!!(很重要)
    db = pymysql.connect("localhost", "用户名", "密码", "数据库名称", use_unicode=True, charset='utf8')
    cursor = db.cursor()

	#储存至数据库
	def save_data(params):
    try:
        sql = 'INSERT INTO toutiao_python VALUES (%s,%s,%s,%s,%s,%s,%s)'
        # 批量插入数据库
        cursor.executemany(sql, params)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


之前直接的想法是查到一条数据储存一条数据,发现效率太低了,仔细想了下,这么好用的语言不可能不能批量储存数据,仔细找了下api 发现cursor.executemany(sql, params)这个方法能批量储存数据,效率提升很多.

最后开个多线程来加快爬虫效率

    # 指定搜索的参数offset范围为[CRAWLER_GO*20,(CRAWLER_END+1)*20]
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



- 运行结果
![](https://i.imgur.com/c8XMtj6.png)






















