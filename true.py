import time
import discord
import random

from constant_config import TESTING
from utils import remove_all
from pairedplayer import PairedPlayer
from seekingpartner import SeekingPartner


class TheReal:
    # static config
    guild:                  discord.Guild
    userblacklist:          list[int]
    roleblacklist:          list[int]
    age_table:              dict[str, dict[str, int]]
    gender_table:           dict[str, dict[str, int]]
    region_table:           dict[str, dict[str, int]]
    expiration_pair_time:   int
    expiration_seek_time:   int

    # variable state
    players:            dict[discord.Member, PairedPlayer]
    currently_paired:   dict[discord.Member, discord.Member]
    pair_channels:      list[discord.abc.GuildChannel]
    seeking_partner_pool: dict[discord.Member, SeekingPartner]


    def __init__(self, guild: discord.Guild, userblacklist: list[int], roleblacklist: list[int], expiration_pair_time: int, expiration_seek_time: int):
        self.guild = guild
        self.userblacklist = userblacklist
        self.roleblacklist = roleblacklist
        self.expiration_pair_time = expiration_pair_time
        self.expiration_seek_time = expiration_seek_time

        self.players = {}
        self.currently_paired = {}
        self.pair_channels = []
        self.seeking_partner_pool = {}


    async def createPrivateChannels(self, memA: discord.Member, memB: discord.Member) -> list[discord.abc.GuildChannel]:
        permissions = {
            memA: discord.PermissionOverwrite(view_channel=True),
            memB: discord.PermissionOverwrite(view_channel=True),
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        private_category = await self.guild.create_category_channel(f"private-{memA.name}-{memB.name}", overwrites=permissions)
        private_text = await self.guild.create_text_channel("private", category=private_category)
        if not TESTING:
            await private_text.send(f"{memA.mention} {memB.mention} HIIIIII")
        private_voice = await self.guild.create_voice_channel("private", category=private_category)
        self.pair_channels += private_category, private_text, private_voice
        return [private_category, private_text, private_voice]
    
    async def pair_all(self) -> int:
        async def thesus(j: SeekingPartner):
            personal_partner_pool = {}

            for amonger in self.seeking_partner_pool.values():
                if j.is_compatible_with(amonger):
                    personal_partner_pool[amonger.member] = amonger
            if len(personal_partner_pool) > 0:
                partner = random.choice(list(personal_partner_pool.keys()))
                await self.pair(j.member, partner)
                return 0

            else:
                return 1
        currently_unpairable = 0
        while currently_unpairable < len(self.seeking_partner_pool):
            currently_unpairable += await thesus(random.choice(list(self.seeking_partner_pool.values())))
        return len(self.seeking_partner_pool)
                
    
    async def clean(self, player: PairedPlayer):
        print(f"player = {player.member.name}")
        try:
            partner = self.currently_paired[player.member]
        except KeyError:
            print("partner was not found, assuming already cleaned up.")
            # del self.players[player.member]
            return

        print(f"partner = {partner.name}")
        for channel in player.pair_channels:
            await channel.delete()

        del self.currently_paired[player.member]
        print(f"{player.member.name}, the player, was removed from currently_paired")
        del self.players[player.member]
        print(f"{player.member.name}, the player, was removed from players")

        # print(f"cleaning up the partner, {partner}")
        del self.currently_paired[partner]
        del self.players[partner]
        # self.clean()
        # print(f"{partner.name}, the partner, was removed from currently_paired")
        # print(f"{partner.name}, the partner, was NOT removed from players")
    
    async def prune_paired(self):
        for member, player in self.players.copy().items():
            # print(f"{member.name} paired {time.time() - player.time_paired} seconds ago")
            if (time.time() - player.time_paired) > self.expiration_pair_time:
                print(f"{member.name}'s time has expired, cleaning")
                await self.clean(player)
            if not member in self.guild.members:
                print(f"{member.name} has left, cleaning")
                await self.clean(player)

    async def prune_seeking(self):
        for member, seeker in self.seeking_partner_pool.copy().items():
            # print(f"{member.name} paired {time.time() - player.time_paired} seconds ago")
            if (time.time() - seeker.time_started_seeking) > self.expiration_seek_time:
                print(f"{member.name}'s time has expired, cleaning")
                del self.seeking_partner_pool[member]
            if not member in self.guild.members:
                print(f"{member.name} has left, cleaning")
                del self.seeking_partner_pool[member]
            
            if self.guild.get_member(member.id).status == discord.Status.offline:
                del self.seeking_partner_pool[member]
            
    
    async def random_single_pair(self, mem: discord.Member):
        member_pool = self.get_member_pool()
        if not mem in member_pool:
            raise ValueError("Member cannot be paired, not in member pool.")
        member_pool = remove_all(member_pool, mem)
        if not member_pool:
            raise ValueError(f"member_pool is falsey, was {mem.name} the last member left?")
        memberalfa, memberbravo = mem, random.sample(member_pool, 1)[0]
        await self.pair(memberalfa, memberbravo)

        print(f"{memberalfa.name} and {memberbravo.name} have been paired.")


    async def pair(self, memberalfa: discord.Member, memberbravo: discord.Member):
        privatechannels = await self.createPrivateChannels(memberalfa, memberbravo)
        current_time = time.time()

        try:
            del self.seeking_partner_pool[memberalfa]
            del self.seeking_partner_pool[memberbravo]
        except Exception as e:
            print(e)

        self.players[memberalfa] = PairedPlayer(memberalfa, privatechannels, current_time)
        self.players[memberbravo] = PairedPlayer(memberbravo, privatechannels, current_time)

        self.currently_paired[memberalfa] = memberbravo
        self.currently_paired[memberbravo] = memberalfa
    
    def is_disallowed(self, member: discord.Member) -> str:
        if member.bot:
            return "bot"
        if member in self.currently_paired.keys():
            return "paired"
        if member in self.seeking_partner_pool.keys():
            return "in seeking partner pool"
        # idk why this is like this
        if self.guild.get_member(member.id).status == discord.Status.offline:
            return "offline"
        for role in member.roles[1:]:
            if role.id in self.roleblacklist:
                return "in role blacklist"
        if member.id in self.userblacklist:
            return "in user blacklist"


        return ""