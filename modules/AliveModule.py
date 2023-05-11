from typing import overload

import platform

import discord
from discord import commands, guild_only

import Container
from BaseModule import BaseModule
from Container import DependencyContainer, Injectable
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
        comms = self.get_commands()
        if message.channel.id != self.config["bot_channel_id"]:
            pass
        if any([mention.id == self.discord_client.user.id for mention in message.mentions]):
            await message.reply("Yes I'm alive!")

    @commands.slash_command()
    async def hello(self, ctx: discord.ApplicationContext):
        """Says hello"""
        channel = self.discord_client.get_channel(self.config["bot_channel_id"])
        await channel.send(content="test command")
        pass



def setup(bot):
    bot.add_cog(AliveModule(bot))



