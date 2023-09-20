import discord

class PairedPlayer:
    member: discord.Member
    pair_channels: list[discord.abc.GuildChannel]
    time_paired: float

    def __init__(self, member: discord.Member, pair_channels: list[discord.abc.GuildChannel], time_paired: float):
        self.member = member
        self.pair_channels = pair_channels
        self.time_paired = time_paired