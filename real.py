import discord
from utils import *
from discord.ext import tasks, commands
from extbot import Bot
from true import TheReal
from seekingpartner import SeekingPartner
import asyncio
from constant_config import *

class congo(commands.Cog):
    bot: Bot
    real: TheReal

    def __init__(self, bot: Bot):
        self.bot = bot
        try:
            self.real = self.bot.state['real']
        except KeyError:
            # does not exist, let on_ready handle it
            pass
        self.pairRemaining.start()

    # ONLY called when the extension is loaded for the FIRST time
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.real = TheReal(guild=self.bot.get_guild(MAIN_SERVER), userblacklist=USER_BLACKLIST, roleblacklist=ROLE_BLACKLIST,
                                expiration_pair_time=EXPIRATION_PAIR_TIME, expiration_seek_time=EXPIRATION_SEEK_TIME)
        self.bot.state['real'] = self.real

    def cog_unload(self):
        self.pairRemaining.cancel()
        self.bot.state['real'] = self.real

    @tasks.loop(seconds=16)
    async def pairRemaining(self):
        try:
            assert(self.real)
        except AttributeError:
            await self.bot.wait_until_ready()
            await asyncio.sleep(0.05)
        
        await self.real.prune_paired()
        await self.real.prune_seeking()
        await self.real.pair_all()
        pass


    @commands.slash_command(name="please_pair_me", description="adds you to the list of members that can be paired")
    async def add_pair_role_command(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        disallowed_reason = self.real.is_disallowed(ctx.author)
        if not disallowed_reason:
            self.real.seeking_partner_pool[ctx.author] = SeekingPartner(ctx.author)
            await ctx.respond(f"Added you to the seeking partner pool, which has {len(self.real.seeking_partner_pool)-1} other members.")
        else:
            await ctx.respond(f"Not added because member is: {disallowed_reason}")

def setup(bot: Bot):
    bot.add_cog(congo(bot))
