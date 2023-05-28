import time

import discord
import os
import subprocess
from discord import commands

from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.ModuleConfig import ModuleConfig


class RemoteManagementModule(BaseModule):

    discord_client: DiscordClient = Injectable[DiscordClient]()

    async def on_load(self):
        pass

    async def on_message(self, message: discord.Message):
        pass

    @commands.guild_only()
    @commands.slash_command(guild_ids=[630432344498503718], description="Shuts down the bot", name="shutdown")
    async def shutdown(self, ctx: discord.ApplicationContext):
        await ctx.response.send_message(content="Shutting down now")
        quit()
        pass

    @commands.guild_only()
    @commands.slash_command(guild_ids=[630432344498503718], description="Restarts the bot while pulling the newest version from git", name="restart")
    async def restart(self, ctx: discord.ApplicationContext):
        await ctx.response.send_message(content="Restarting now...")
        time.sleep(1)
        path = os.getcwd() + "/start.sh"
        subprocess.Popen([path])
        pass


def setup(bot):
    bot.add_cog(RemoteManagementModule(bot))
