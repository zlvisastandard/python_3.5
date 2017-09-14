##十行代码,让你秒回女友信息

作为程序员我们的生活就是coding,coding ,每天就是加班加班,前一阵子一朋友(程序员)身上发生了悲催的事: 
事情的经过大概是,他加班比较忙,没时间看微信,女友找他有事,发了一堆微信给他,他没看手机,所以一条消息都没回,结果女友大怒,说他心里只有工作,
然后跟他闹分手,他又比较内敛,不擅长言语,不知道怎样哄女生,最后找到我这来诉苦,我想了下,给了他好的解决方法,用程序员的方式来解决问题  
事情的起因是他没有秒回微信消息,那为什么不写个程序,加个机器人秒回消息呢?  想到这里记起来微信是提供python api的.  
#####需要的东西:  
1. python3.5环境
2. 微信api
3. 聊天机器人

####看代码

from wxpy import *
	
	#cache_path 保存生成的二维码,不用每次都生成二维码
	bot = Bot(cache_path=True)
	# 获取好友列表
	friends = bot.friends()
	for friend in friends:
    	print(friend)
	params = []
	# 获取组群 谨慎使用
	# groups = bot.groups()
	# for group in groups:
	#     print(group)

	# group = groups.search('聊天组名称')[0]
	# params.append(group)
	# group.send('test!')

	friend = friends.search('女友名称')[0]
	params.append(friend)
	#登陆后先主动发一条消息过去
	# friend.send('随便问我一个问题我都知道答案')
	tuiling = Tuling(api_key='注册的图灵key')


	@bot.register(params, msg_types=TEXT)
	def reply_my_friend(msg):
    	tuiling.do_reply(msg)


	embed()


用的[wxpy](https://github.com/youfou/wxpy "wxpy"),这个库还可以有很多玩发,简单好用  
启动程序,会出现二维码,直接用手机微信扫下就可以登陆了
![](https://i.imgur.com/K2WuzuX.png)

登陆后就可以看到好友列表和聊天组列表了,这个时候指定的用户和聊天组可以收到一条消息,用params数组可以添加多个聊天对象和聊天群
![](https://i.imgur.com/2KKCM4P.png)


现在还不能自动回复消息进行聊天,加入一个聊天机器人就可以愉快的玩耍了,这里是接入的图灵机器人,先去图[灵机器人官网](http://www.tuling123.com/ "灵机器人官网")注册账号,创建自己的机器人
![](https://i.imgur.com/cL9wfBm.png)
注册完后会获取一个key,我们代码里面只需要这个key就够了

![](https://i.imgur.com/wKEXRO3.png)

代码里面用到这里

![](https://i.imgur.com/cT2g0Rt.png)


现在重新启动就将我们的微信好托管给图灵机器人了,他可以帮我们秒回消息



- 运行结果:
![](https://i.imgur.com/jsUyrSF.jpg)


源代码见[GitHub](https://github.com/panic-java/python_3.5/tree/master/wechartauto "GitHub")


















    




