import glob
import io

import discord
import matplotlib.pyplot as plt
from PIL import Image
from discord.ext import commands
from matplotlib.dates import date2num, DateFormatter

import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, ConciseDateFormatter, AutoDateLocator
from datetime import datetime
from discord.utils import get

from enum import Enum
import numpy as np
from scipy.interpolate import CubicSpline
from statsmodels.nonparametric.smoothers_lowess import lowess

from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.CoffeeLog import CoffeeLog, CoffeeType
from dependencies.ModuleConfig import ModuleConfig

class KafoView(discord.ui.View):

    log: CoffeeLog
    config: ModuleConfig
    bot: DiscordClient

    selected_count: int = 1

    def save_kafo(self, user_id: int, t: CoffeeType, drink_count: int) -> int:
        for i in range(drink_count):
            self.log.add_coffee(user_id, t)
        return sum([x.kind.value for x in self.log.data[user_id]])

    def create_stats(self) -> io.BufferedIOBase:
        # Separate x (datetime) and y (enum values) data

        # Extract timestamps and enum values for each data set
        timestamps_sets = [[date2num(item.timestamp) for item in self.log.data[id]] for id in self.log.data]
        enum_values_sets = [[item.kind.value for item in self.log.data[id]] for id in self.log.data]
        label_sets = [id for id in self.log.data]

        data_sets = list(zip(timestamps_sets, enum_values_sets, label_sets))
        data_sets.sort(key=lambda x: len(x[0]), reverse=True)

        timestamps_sets, enum_values_sets, label_sets = zip(*data_sets)
        timestamps_sets = list(timestamps_sets)
        enum_values_sets = list(enum_values_sets)
        label_sets = list(label_sets)

        cumulative_sum_sets = [np.cumsum(enum_values) for enum_values in enum_values_sets]
        fig, ax = plt.subplots()

        for i, user_id in enumerate(label_sets):
            timestamps = timestamps_sets[i]
            data = cumulative_sum_sets[i]
            user = get(self.bot.get_all_members(), id=user_id)
            if user:
                plt.plot(timestamps, data, label=(user.display_name + " (" + str(data[-1]) + ")"))

        # Set labels and title
        ax.set_xlabel('Datum')
        ax.set_ylabel('Počet káviček')
        ax.set_title('Kafo staty by Kultivátor®')

        ax.xaxis.set_major_formatter(DateFormatter('%d. %b'))

        plt.xticks(rotation=45)

        plt.legend()
        plt.grid()

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    async def handle_kafo(self, user_id: int, count: CoffeeType, interaction: discord.interactions.Interaction):
        count = self.save_kafo(user_id, count, self.selected_count)
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

    @discord.ui.button(label="Energy", style=discord.ButtonStyle.secondary, emoji="<:kenneth:578950451379044364>")
    async def energy(self, button, interaction: discord.interactions.Interaction):
        await self.handle_kafo(interaction.user.id, CoffeeType.ENERGY, interaction)

    @discord.ui.button(label="Stats", style=discord.ButtonStyle.secondary, emoji="📈")
    async def stats(self, button, interaction: discord.interactions.Interaction):
        image = self.create_stats()
        await interaction.message.edit(content="",file=discord.File(image, "kafo.png"), view=None)

    @discord.ui.string_select(options=[
        discord.SelectOption(label="1 nápoj", default=True, value="1"),
        discord.SelectOption(label="2 nápoje", value="2"),
        discord.SelectOption(label="3 nápoje", value="3"),
        discord.SelectOption(label="4 nápoje", value="4"),
        discord.SelectOption(label="5 nápojů", value="5")],
        placeholder="Vyber si počet <:kafo:780424664152408074>")
    async def count_selected(self, select, interaction: discord.interactions.Interaction):
        self.selected_count = int(select.values[0])
        await interaction.response.defer()
        pass


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
    @commands.slash_command(description="Čas na kávičku ☕", name="kafo")
    async def kafo(self, ctx: discord.ApplicationContext, kind: discord.Option(str, "Text entry (for legacy devices)", required=False, choices=["kafo", "double", "energy", "stats"]), count: discord.Option(int, "Number of drinks", required=False, default=1)):
        view = KafoView()
        view.log = self.log
        view.bot = self.bot
        view.config = self.config
        if kind is None or "":
            await ctx.response.send_message(view=view)
            return
        match kind:
            case "kafo":
                count = view.save_kafo(ctx.user.id, CoffeeType.NORMAL, count)
            case "double":
                count = view.save_kafo(ctx.user.id, CoffeeType.DOUBLE, count)
            case "energy":
                count = view.save_kafo(ctx.user.id, CoffeeType.ENERGY, count)
            case "stats":
                await ctx.response.send_message(file=discord.File(view.create_stats(), "kafo.png"))
                return
        await ctx.response.send_message(content=f"Kafe číslo: {count}\nNa zdraví <:kafo:780424664152408074>")

        pass


def setup(bot):
    bot.add_cog(KafoModule(bot))
