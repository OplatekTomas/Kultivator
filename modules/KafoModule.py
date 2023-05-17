import datetime
import platform

import platform


import discord
from discord.commands import slash_command
from discord.ext import commands


from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.PersistentStorage import PersistentStorage
from dependencies.ModuleConfig import ModuleConfig

class KafoView(discord.ui.View):

    config: ModuleConfig

    async def handle_kafo(self, user_id: int, count: int, interaction: discord.interactions.Interaction):
        count = self.save_kafo(user_id, count)
        await interaction.message.edit(content=f"Kafe číslo: {count}\nNa zdraví <:kafo:780424664152408074>", view=None)


    def save_kafo(self, user_id: int, count: int) -> int:
        if "score" not in self.config:
            self.config["score"] = {}
        if str(user_id) not in self.config["score"]:
            self.config["score"][str(user_id)] = 0
        current = self.config["score"][str(user_id)] + count
        self.config["score"][str(user_id)] = current
        self.config.save()
        return current

    @discord.ui.button(label="Kávička", style=discord.ButtonStyle.secondary, emoji="<:kafo:780424664152408074>")
    async def depresso_callback(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, 1, interaction)

    @discord.ui.button(label="Double depresso", style=discord.ButtonStyle.secondary, emoji="<:void:1030795344113565697>")
    async def double_depresso(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, 2, interaction)

    @discord.ui.button(label="Hahad", style=discord.ButtonStyle.secondary, emoji="<:hahad:908660929472905226>")
    async def hahad(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, 1, interaction)

    @discord.ui.button(label="Stats", style=discord.ButtonStyle.secondary, emoji="📈")
    async def stats(self, button, interaction: discord.interactions.Interaction):
        await interaction.message.edit(content="Pomalu snejksi, staty jsem ještě neimplmenetoval <:harold:762400725123989525>", view=None)



class KafoModule(BaseModule):

    discord_client: DiscordClient = Injectable[DiscordClient]()
    config: ModuleConfig = Injectable[ModuleConfig]()
    storage: PersistentStorage = Injectable[PersistentStorage]()

    async def on_load(self):
        pass

    async def on_message(self, message: discord.Message):
        if message.content.startswith("!kafo"):
            await message.reply("The correct use is /kafo. Yes there is a command now")

    @commands.guild_only()
    @commands.slash_command(guild_ids=[630432344498503718], description="Čas na kávičku ☕", name="kafo")
    async def kafo(self, ctx: discord.ApplicationContext):
        view = KafoView()
        view.config = self.config
        await ctx.response.send_message(view=view)
        pass


def setup(bot):
    bot.add_cog(KafoModule(bot))
