from chatterbotapi import ChatterBotFactory, ChatterBotType
from bot import Bot

factory = ChatterBotFactory()

bot1 = Bot("cleverbot")
bot1sesh = bot1.start_session(bot1)

bot2 = Bot("pandorabots")
bot2sesh = bot2.start_session(bot2)

start = "How are you?"

while (1):
    print 'bot1>' + start
    start = bot2sesh.think(start)
    print 'bot2>' + start
    start = bot1sesh.think(start)
