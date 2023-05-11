from BotConfig import *
from DiscordClient import *
import faulthandler

faulthandler.enable()


if __name__ == '__main__':
    config = BotConfig.load()

    discord = DiscordClient(config=config)
    discord.run(config.key)


    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
