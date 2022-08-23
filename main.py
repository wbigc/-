from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():


  wordList=['你要尽全力保护你的梦想。那些嘲笑你的人，他们必定会失败，他们想把你变成和他们一样的人。如果你有梦想的话，就要努力去实现。——《当幸福来敲门》','生命可以归结为一种简单的选择，要么忙于生存，要么赶着去死。——《肖申克的救赎》'，'如果做人没有梦想，那跟咸鱼有什么分别？——《少林足球》'，'死亡不是生命的终点，遗忘才是。——《寻梦环游记》'，'走人生的路就像爬山一样，看起来走了许多冤枉的路，崎岖的路，但最终会到达山顶。——《城南旧事》'，'我不会关注别人的赞美或者诋毁。我只在意自己的感觉。——《莫扎特传》'，'傲慢让别人无法靠近我，偏见让我无法靠近别人。——《傲慢与偏见》'，'没有什么事情是肯定的，这也是我唯一能肯定的事情。——《美丽心灵》'，'如果我放弃，就是向那些错看我的人屈服。——《叫我第一名》'，'世界上最大的谎言就是你不行。——《垫底辣妹》'，'这些墙不是为了把问题关在外面才修建的，你需要面对它。——《音乐之声》'，'上天没有给你想要的，不是因为你不配，而是你值得拥有更好的。——《乱世佳人》'，'星星在哪里都是很亮的，就看你有没有抬头去看它们。——《玻璃樽》'，'不管前方的路有多苦，只要走的方向正确，不管多么崎岖不平，都比站在原地更加接近幸福。——《千与千寻》'，'我听别人说这世界上有一种鸟是没有脚的，它只能够一直的飞呀飞呀，飞累了就在风里面睡觉，这种鸟一辈子只能下地一次，那一次就是它死亡的时候。——《阿飞正传》'，'记住，你是能让世界洒满阳光的人。——《白雪公主与七个小矮人》'， '生活就像一盒巧克力，你永远不知道你会得到什么。——《阿甘正传》'，'如果记忆是一个罐头，我希望它永远不会过期。——《重庆森林》'，'一只蛋如果从外面被敲开，注定只能被吃掉。如果从里面啄开，说不定是只鹰。——《长津湖》'，兽人，永不为奴。——《魔兽》'，'注意你的思想，它将变成你的言辞；注意你的言辞，它将变成你的行动；注意你的行动，它将变成你的习惯；注意你的习惯，它将变成你的人格；注意你的人格，它将变成你的命运。——《铁娘子》'，'只要你肯领略，就会发现人生本是多么可爱，每个季节里有很多足以让你忘记所有烦恼的赏心乐趣。——《陆小凤传奇》'，'当你年轻时，以为什么都有答案，可是老了的时候，你可能又觉得其实人生并没有所谓的答案。每天你都有机会和很多人擦身而过，有些人可能会变成你的朋友或者是知己，所以我从来没有放弃任何跟人磨擦的机会。有时候搞得自己头破血流，管他呢！开心就行了。——《堕落天使》'，'开拓视野，冲破艰险，看见世界，身临其境，贴近彼此，感受生活，这就是生活的目的。——《白日梦想家》'，'从现在起，你必须学会一件事，你不能靠别人只能靠自己，只能依靠你自己，很悲哀，但这是真的，你最好早点学会这件事情。——《美国丽人》'，'凡事都有可能，永远别说永远。——《放牛班的春天》'，'在从前，当一个人心里有个不可告人的秘密，他会跑到深山里，找一棵树，在树上挖个洞，将秘密告诉那个洞，再用泥土封起来，这个秘密就永远没人知道。——《2046》'，'如果再也不能见到你，祝你早安，午安，晚安。——《楚门的世界》'，'我希望你能活出最精彩的自己，我希望你能见识到令你惊奇的事物，我希望你能体验从未有过的情感，我希望你能遇见一些想法不同的人，我希望你为你自己的人生感到骄傲 。如果你发现自己还没有做到，我希望你有勇气重头再来。——《本杰明巴顿奇事》'，'我们读诗写诗，非为它的灵巧。我们读诗写诗，因为我们是人类的一员。而人类充满了热情。医药，法律，商业，工程，这些都是高贵的理想，并且是维生的必需条件。但是诗，美，浪漫，爱，这些才是我们生存的原因。——《死亡诗社》'，'不知道从什么时候开始，在什么东西上面都有个日期，秋刀鱼会过期，肉罐头会过期，连保鲜纸都会过期，我开始怀疑，在这个世界上，还有什么东西是不会过期的？——《重庆森林》'，'如果你不出去走走，你就会以为这就是全世界。——《天堂电影院》'， '如果我不顾一切发挥每一点潜能去做会怎样？我必须做到，我别无选择。——《风雨哈佛路》'，'你真正是谁并不重要，重要的是你的所做所为。——《蝙蝠侠：开战时刻》'，'有信心不一定会成功，没信心一定不会成功。——《英雄本色》'，'你们一直抱怨这个地方，但是你们却没有勇气走出这里。——《飞越疯人院》'，'阴影，也是你人生的一部分。——《心花路放》'，'时间很贪婪——有时候，它会独自吞噬所有的细节。——《追风筝的人》'，'你的心是自由的，要有勇气追求自由。——《勇敢的心》'，'决定我们成为什么样人的，不是我们的能力，而是我们的选择。——《哈利·波特与密室》'，'希望是一个好东西，也许是最好的东西，好东西是不会消亡的。——《肖申克的救赎》'，'有些人能清楚地听到自己内心深处的声音，并以此行事。这些人要么变成了疯子，要么成为传奇。——《秋日传奇》'，'人生也许就是不断地放下，然而令人痛心的是，我都没能好好地与他们道别。——《少年派的奇幻漂流》'，'有时候你只需要花二十秒，疯狂地一鼓作气。仅仅花上二十秒，鼓起勇气，即便有多尴尬。然后我向你保证，会有好事发生的。——《我家买了动物园》'，'你唯一的对手，就是昨天的自己。——《Coco寻梦环游记》',' 没有人的人生是完美的，但生命的每一刻都是美丽的。 无论什么样的灾难降临，只要生命还在，生活始终要继续。 活着，就是最美丽的事。--《美丽人生》','我爱你不是因为你是谁，而是我在你面前可以是谁。——《剪刀手爱德华》','愿意陪你长大的人已不多， 何况还要陪你变老。 ——《春娇救志明》']
  return  wordList[random.randint(0,len(wordList)-1]          

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
data = {"weather":{"value":wea,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(),"color":get_random_color()},"highest": {"value":highest,"color":get_random_color()},"lowest":{"value":lowest, "color":get_random_color()}}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
