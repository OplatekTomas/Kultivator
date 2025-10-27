import asyncio
from sys import stdout

import discord
from discord import commands

from BaseDependencies import SingletonDependency
from BaseModule import BaseModule
from Container import Injectable
from DiscordClient import DiscordClient
from dependencies.ModuleConfig import ModuleConfig
from dependencies.WashingMachineAPI import WashingMachineAPI


class WashingMachineModule(BaseModule):

    washing_machine: WashingMachineAPI = Injectable[WashingMachineAPI]()
    discord_client: DiscordClient = Injectable[DiscordClient]()
    config: ModuleConfig = Injectable[ModuleConfig]()

    previous_running_state: bool = False
    assigned_user = None

    async def on_load(self):
        channel_id = self.config["channel_id"]
        channel = self.discord_client.get_channel(channel_id)
        
        # State tracking for whether the washing machine was running in the previous cycle
        self.previous_running_state = self.washing_machine.is_running()
        # Background task for monitoring the washing machine status
        async def monitor_washing_machine():
            while True:
                await asyncio.sleep(1)  # Check every second
                current_state = self.washing_machine.is_running()

                if self.previous_running_state and not current_state:
                    if self.assigned_user is None:
                        await channel.send("@everyone dojela pračka ")
                    else:
                        self.assigned_user = None
                        await channel.send(f"@{self.assigned_user} dojela pračka ")

                # Update the previous state
                self.previous_running_state = current_state

        # Start the monitoring task
        asyncio.create_task(monitor_washing_machine())

    async def on_message(self, message: discord.Message):
        pass

    @commands.guild_only()
    @commands.slash_command(description="Jede pračka?", name="iswashing")
    async def is_running(self, ctx: discord.ApplicationContext):
        await ctx.send_response(self.washing_machine.is_running())
        pass

    @commands.guild_only()
    @commands.slash_command(description="Zapl jsem pracku", name="peru")
    async def assign_user(self, ctx: discord.ApplicationContext):
        self.assigned_user = ctx.author.display_name
        await ctx.send_response(f"Další pračka je od {self.assigned_user}")
        pass


def setup(bot):
    bot.add_cog(WashingMachineModule(bot))
