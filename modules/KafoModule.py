import platform

import platform


import discord
from discord.commands import slash_command
from discord.ext import commands


from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.ModuleConfig import ModuleConfig


class KafoModule(BaseModule):

    discord_client: DiscordClient = Injectable[DiscordClient]()
    config: ModuleConfig = Injectable[ModuleConfig]()

    async def on_load(self):
        pass

    async def on_message(self, message: discord.Message):
        if message.content.startswith("!kafo"):
            await message.reply("The correct use is /kafo. Yes there is a command now")

    @slash_command(guild_ids=[630432344498503718], description="Čas na kávičku")
    @commands.guild_only()
    async def kafo(self, ctx: discord.ApplicationContext, cmd: discord.Option(str, choices=['', 'stats'])):
        if "score" not in self.config:
            self.config["score"] = {}
        if str(ctx.author.id) not in self.config["score"]:
            self.config["score"][str(ctx.author.id)] = 0
        self.config["score"][str(ctx.author.id)] = self.config["score"][str(ctx.author.id)] + 1
        self.config.save()
        await ctx.response.send_message("You drank " +  str(self.config["score"][str(ctx.author.id)]) + " coffees " + self.config["kafo_response"])
        pass
def setup(bot):
    bot.add_cog(KafoModule(bot))
