from utils.fetches import config

class State:
    def __init__(self):
        self.token: str = config.token()
        self.prefix: str = config.prefix()
        self.testing: int = config.testing()
        self.all_guilds: list[int]
        self.ban_guilds: list[int] = config.ban_guilds()
        self.ban_users: list[int] = config.ban_users()
        self.dev_guilds: list[int] = config.dev_guilds()
        self.dev_users: list[int] = config.dev_users()

    def add_guild(self, guild_id: int):
        if guild_id not in self.all_guilds:
            self.all_guilds.append(guild_id)

    def del_guild(self, guild_id: int):
        if guild_id in self.all_guilds:
            self.all_guilds.remove(guild_id)

    def add_ban_guild(self, guild_id: int):
        if guild_id not in self.ban_guilds:
            self.ban_guilds.append(guild_id)

    def del_ban_guild(self, guild_id: int):
        if guild_id in self.ban_guilds:
            self.ban_guilds.remove(guild_id)

    def add_ban_user(self, user_id: int):
        if user_id not in self.ban_users:
            self.ban_users.append(user_id)

    def del_ban_user(self, user_id: int):
        if user_id in self.ban_users:
            self.ban_users.remove(user_id)

    def add_dev_guild(self, guild_id: int):
        if guild_id not in self.dev_guilds:
            self.dev_guilds.append(guild_id)

    def del_dev_guild(self, guild_id: int):
        if guild_id in self.dev_guilds:
            self.dev_guilds.remove(guild_id)

    def add_dev_user(self, user_id: int):
        if user_id not in self.dev_users:
            self.dev_users.append(user_id)

    def del_dev_user(self, user_id: int):
        if user_id in self.dev_users:
            self.dev_users.remove(user_id)

state: State = State()