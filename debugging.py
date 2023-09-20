import discord
from utils import *
from discord.ext import commands
from extbot import Bot
from true import TheReal
from seekingpartner import SeekingPartner
from constant_config import *
import asyncio

class dbg(commands.Cog):
    bot: Bot
    real: TheReal

    def __init__(self, bot: Bot):
        self.bot = bot
        try:
            self.real = self.bot.state['real']
        except KeyError:
            # does not exist, let on_ready handle it
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(0.005)
        # real.py should have created this by now
        self.real = self.bot.state['real']

    def cog_unload(self):
        self.bot.state['real'] = self.real


    @commands.slash_command(guild_ids=[MAIN_SERVER], name="manual_clean", description="clear one user and their partner", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def singlecleancommand(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member)):
        await ctx.interaction.response.defer()
        await self.real.clean(self.real.players[member])
        await ctx.respond(f"cleaned up {member.name} and their partner")

    @commands.slash_command(name="dumb_clean", description="delete all channels that start with 'private'", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def dumbclean(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        for channel in ctx.guild.channels:
            if channel.name.startswith("private"):
                await channel.delete()
        await ctx.respond("deleted all private")

    @commands.slash_command(guild_ids=[MAIN_SERVER], name="clean_old", description="clean up channels that aren't in the pair_channels list", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def old_clean_command(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        for channel in ctx.guild.channels:
            if channel.name.startswith("private"):
                if not channel in self.real.pair_channels:
                    await channel.delete()
        await ctx.respond("deleted all private that were not in pair_channels")




    @commands.slash_command(name="invoke_pair_single", description="randomly pair a specific member", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def single_pair_command(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member)):
        await ctx.interaction.response.defer()
        await self.real.random_single_pair(member)
        await ctx.respond(f"paired {member.name}")

    @commands.slash_command(name="invoke_pair_all", description="pairs all users and gives them private channels together", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def paircommand(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        remaining = await self.real.pair_all()
        if remaining:
            await ctx.respond(f"Paired members, {remaining} remains.")
        else:
            await ctx.respond(f"Paired members, none remain.")






    @commands.slash_command(guild_ids=[MAIN_SERVER], name="manual_pair", description="manually pair two specific members together", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def manual_pair_command(self, ctx: discord.ApplicationContext, membera: discord.Option(discord.Member), memberb: discord.Option(discord.Member)):
        await ctx.interaction.response.defer()
        await self.real.pair(membera, memberb)
        await ctx.respond(f"paired {membera.name} and {memberb.name}")

    
    @commands.slash_command(guild_ids=[MAIN_SERVER], name="manual_please_pair", description="adds a member to the list of members that can be paired", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def manual_please_pair(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member)):
        await ctx.interaction.response.defer()
        disallowed_reason = self.real.is_disallowed(member)
        if not disallowed_reason:
            self.real.seeking_partner_pool[member] = SeekingPartner(member)
            await ctx.respond(f"Added {member.name} to the seeking partner pool, which has {len(self.real.seeking_partner_pool)-1} other members.")
        else:
            await ctx.respond(f"Not added because {member.name} is: {disallowed_reason}")



    @commands.slash_command(guild_ids=[MAIN_SERVER], name="show_seeking", description="show members in seeking_partner_pool", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def show_seeking(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        mstr = "{\n"
        for amonger in self.real.seeking_partner_pool.values():
            mstr += f"{amonger.member.name}:\ngender: `{amonger.gender}` age: `{amonger.age}` region: `{amonger.region}`\nseek_gender: `{amonger.seek_gender}` seek_age: `{amonger.seek_age}` seek_region: `{amonger.seek_region}`\n\n"
        mstr += "}"
        await ctx.respond(mstr)
    
    @commands.slash_command(guild_ids=[MAIN_SERVER], name="show_pairings", description="show everyone who is paired and their partners", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def showpaired(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        s = "{\n"
        for member, partner in self.real.currently_paired.items():
            s += f"{member.name}: {partner.name}\n"
        s += "}"
        await ctx.respond(s)
    




    @commands.slash_command(name="list_member_compatible", description="list what other members in the seeking partner pool the given member is compatible with",)
    async def fdj(self, ctx: discord.ApplicationContext, member: discord.Option(discord.Member)):
        await ctx.response.defer()
        for mem in ctx.guild.members:
            if self.real.is_allowed(mem):
                self.real.seeking_partner_pool[mem] = SeekingPartner(mem)
        personal_partner_pool = {}
        amonger = self.real.seeking_partner_pool[member]
        for potential_partnerM,potential_partnerS in self.real.seeking_partner_pool.items():
            if amonger.is_compatible_with(potential_partnerS):
                personal_partner_pool[potential_partnerM] = potential_partnerS
        
        amongstring = f"Member {member.name} is compatible with: "
        for compatible_potential_partner in personal_partner_pool:
            amongstring += compatible_potential_partner.name + ", "
        await ctx.respond(amongstring)

    @commands.slash_command(name="check_compatiblity", description="checks to see if 2 given members are compatible with each other",)
    async def thesus(self, ctx: discord.ApplicationContext, membera: discord.Option(discord.Member), memberb: discord.Option(discord.Member)):
        m,n = SeekingPartner(membera), SeekingPartner(memberb)
        await ctx.respond(f"{membera.name} and {memberb.name} are compatible: {m.is_compatible_with(n)}")






    @commands.slash_command(name="clean", description="unpair all users and delete their respective channels", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def cleancommand(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        while self.real.players:
            p = list(self.real.players.values())[0]
            await self.real.clean(p)
        await ctx.respond("cleaned up")


def setup(bot: Bot):
    bot.add_cog(dbg(bot))
    