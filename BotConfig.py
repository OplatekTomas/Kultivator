from __future__ import annotations

import json
import types
from typing import List, Dict


class BotConfig():
    config_file: str = "config.json"
    key: str
    client: str
    servers: []
    module_configs: Dict[str, Dict]

    def __init__(self, key: str, client: str, servers: [], module_configs: Dict[str, Dict]):
        self.servers = servers
        self.client = client
        self.key = key
        self.module_configs = module_configs

    @staticmethod
    def load() -> BotConfig:
        required_keys = [["key", ""], ["client", ""], ["servers", list()], ["modules", dict()]]
        should_update_config_file = False
        config: BotConfig = None
        with open(BotConfig.config_file, "r") as f:
            json_data = json.load(f)
            for key, default_value in required_keys:
                if key not in json_data:
                    json_data[key] = default_value
                    should_update_config_file = True
            config = BotConfig(
                key=json_data['key'],
                client=json_data['client'],
                servers=json_data['servers'],
                module_configs=json_data["modules"]
            )
        if should_update_config_file:
            with open(BotConfig.config_file, "w") as f:
                json_str = json.dumps(json_data, indent=2)
                f.write(json_str)
        return config

    def handle_config_creation(self, module: str):
        if module not in self.module_configs:
            self.module_configs[module] = dict()
        pass

    def save(self):
        json_dict = {
            "key": self.key,
            "servers": self.servers,
            "client": self.client,
            "modules": self.module_configs
        }
        with open(BotConfig.config_file, "w") as f:
            json_str = json.dumps(json_dict, indent=2)
            f.write(json_str)
