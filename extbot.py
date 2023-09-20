import discord

class MyBot(discord.Bot): # subclass discord.Bot
    state: dict[any, any]
    def __init__(self, description=None, *args, **options):
        self.state = {}
        super().__init__(description, *args, **options)

Bot = MyBot