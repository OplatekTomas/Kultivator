import discord
from discord.ext import commands



class BaseModule(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    async def on_load(self):
        pass

    async def on_message(self, message: discord.Message):
        pass
