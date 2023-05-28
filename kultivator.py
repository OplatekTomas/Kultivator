from BotConfig import *
from DiscordClient import *
import faulthandler

faulthandler.enable()

config = BotConfig.load()

bot = DiscordClient(config=config)
bot.run(config.key)


