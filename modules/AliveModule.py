import platform

import platform


import discord
from discord.commands import slash_command
from discord.ext import commands


from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.ModuleConfig import ModuleConfig


class AliveModule(BaseModule):

    discord_client: DiscordClient = Injectable[DiscordClient]()
    config: ModuleConfig = Injectable[ModuleConfig]()

    async def on_load(self):
        channel = self.discord_client.get_channel(self.config["bot_channel_id"])
        msg = "> Logged in from " + platform.node() + " on " + platform.release()
        await channel.send(content=msg)
        pass

    async def on_message(self, message: discord.Message):
        if message.channel.id != self.config["bot_channel_id"]:
            return
        if any([mention.id == self.discord_client.user.id for mention in message.mentions]):
            await message.reply("Yes I'm alive!")


def setup(bot):
    bot.add_cog(AliveModule(bot))



