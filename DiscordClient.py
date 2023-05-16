from typing import Any

import discord.ext.commands
from discord import Intents
from discord.ext import commands

from BotConfig import BotConfig
from ModuleLoader import ModuleLoader


class DiscordClient(discord.Bot):

    module_loader: ModuleLoader

    def __init__(self, config: BotConfig, **options: Any):
        super().__init__(intents=discord.Intents.all())
        self.module_loader = ModuleLoader(client=self, config=config)

    async def on_ready(self):
        self.module_loader.init_di_container()
        self.module_loader.load_dependencies()
        await self.module_loader.import_modules()

        for module in self.module_loader.modules:
            await module.on_load()

    async def on_message(self, message):
        if message.author.id == self.application_id:
            return
        klt_bot_room = 763901318468730910
        if message.channel.id != klt_bot_room:
            return
        print(f'Message from {message.author}: {message.content}')
        for module in self.module_loader.modules:
            await module.on_message(message)

