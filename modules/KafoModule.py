import datetime
import glob
import platform

import platform
from enum import Enum
from os import walk
from typing import Dict, List

import discord
from discord.commands import slash_command
from discord.ext import commands


from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.CoffeeLog import CoffeeLog, CoffeeType
from dependencies.PersistentStorage import PersistentStorage
from dependencies.ModuleConfig import ModuleConfig

class KafoView(discord.ui.View):

    log: CoffeeLog
    config: ModuleConfig

    def save_kafo(self, user_id: int, t: CoffeeType) -> int:
        self.log.add_coffee(user_id, t)
        return sum([x.kind.value for x in self.log.data[user_id]])

    async def handle_kafo(self, user_id: int, count: CoffeeType, interaction: discord.interactions.Interaction):
        count = self.save_kafo(user_id, count)
        await interaction.message.edit(content=f"Kafe číslo: {count}\nNa zdraví <:kafo:780424664152408074>", view=None)

    @discord.ui.button(label="Kávička", style=discord.ButtonStyle.secondary, emoji="<:kafo:780424664152408074>")
    async def depresso_callback(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, CoffeeType.NORMAL, interaction)

    @discord.ui.button(label="Double depresso", style=discord.ButtonStyle.secondary, emoji="<:void:1030795344113565697>")
    async def double_depresso(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, CoffeeType.DOUBLE, interaction)

    @discord.ui.button(label="Hahad", style=discord.ButtonStyle.secondary, emoji="<:hahad:908660929472905226>")
    async def hahad(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, CoffeeType.INSTINCT, interaction)

    @discord.ui.button(label="Stats", style=discord.ButtonStyle.secondary, emoji="📈")
    async def stats(self, button, interaction: discord.interactions.Interaction):
        await interaction.message.edit(content="Pomalu snejksi, staty jsem ještě neimplmenetoval <:harold:762400725123989525>", view=None)


class KafoModule(BaseModule):

    discord_client: DiscordClient = Injectable[DiscordClient]()
    log: CoffeeLog = Injectable[CoffeeLog]()
    config: ModuleConfig = Injectable[ModuleConfig]()

    async def on_load(self):
        pass

    def after_inject(self):
        pass

    async def on_message(self, message: discord.Message):
        if message.content.startswith("!kafo"):
            await message.reply("The correct use is /kafo. Yes there is a command now")


    def load_cache(self):
        if self.cache is None:
            return
        dir = self.storage.create_dir(self.config["dir"])
        print(glob.glob(f"/home/adam/*.{self.config['ext']}"))

        pass

    @commands.guild_only()
    @commands.slash_command(guild_ids=[630432344498503718], description="Čas na kávičku ☕", name="kafo")
    async def kafo(self, ctx: discord.ApplicationContext):
        view = KafoView()
        view.log = self.log
        view.config = self.config
        await ctx.response.send_message(view=view)
        pass


def setup(bot):
    bot.add_cog(KafoModule(bot))
