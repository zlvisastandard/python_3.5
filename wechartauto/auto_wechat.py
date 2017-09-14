#!/usr/bin/env python
# coding:utf-8

from wxpy import *

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

# group = groups.search('等你回复')[0]
# params.append(group)
# group.send('test!')

friend = friends.search('好友名称')[0]
params.append(friend)
# friend.send('随便问我一个问题我都知道答案')

#此行代码只能放在这里
tuiling = Tuling(api_key='注册的图灵key')

@bot.register(params, msg_types=TEXT)
def reply_my_friend(msg):
    tuiling.do_reply(msg)


embed()
