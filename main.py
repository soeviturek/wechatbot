from wxpy import *

bot = Bot()


my_friends = bot.friends()
target = my_friends.search('阿蓝')[0]
# target.send('Hi，微信机器人lei了')

while True:
    print()

