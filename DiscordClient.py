import logging
from logging import handlers
from typing import Any

import discord.ext.commands
from discord import Intents
from discord.ext import commands

from BotConfig import BotConfig
from ModuleLoader import ModuleLoader


class DiscordClient(discord.Bot):

    module_loader: ModuleLoader

    def __init__(self, config: BotConfig):
        super().__init__(intents=discord.Intents.all())
        self.module_loader = ModuleLoader(client=self, config=config)
        self.module_loader.init_di_container()
        self.module_loader.load_dependencies()
        self.module_loader.import_modules()

        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        log_handler = handlers.TimedRotatingFileHandler('kultivator.log', when='D', interval=1)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s'))
        logger.addHandler(log_handler)

    async def on_ready(self):
        for module in self.module_loader.modules:
            await module.on_load()

    async def on_message(self, message):
        if message.author.id == self.application_id:
            return
        print(f'Message from {message.author}: {message.content}')
        for module in self.module_loader.modules:
            await module.on_message(message)

