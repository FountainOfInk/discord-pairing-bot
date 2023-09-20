import discord
import time
from constant_config import age_table, gender_table, region_table

class SeekingPartner:
    member: discord.Member
    
    gender: str
    age: str
    region: str

    seek_gender: list[str]
    seek_age: list[str]
    seek_region: list[str]

    time_started_seeking: float

    def __init__(self, member: discord.Member):
        self.member = member
        self.time_started_seeking = time.time()

        p=[]
        for table in [age_table, gender_table, region_table]:
            p.append(get_attr_have(self.member, table))
        self.age, self.gender, self.region = p[0], p[1], p[2]
        p=[]
        for table in [age_table, gender_table, region_table]:
            p.append(get_attr_seek(self.member, table))
        self.seek_age, self.seek_gender, self.seek_region = p[0], p[1], p[2]

    
    def is_compatible_with(self, potential_partner: 'SeekingPartner') -> bool:
        def compat(A: 'SeekingPartner', B: 'SeekingPartner'):
            if A == B:
                return False
            for a_seek,b_have in [(A.seek_age,B.age), (A.seek_gender, B.gender), (A.seek_region, B.region)]:
                if "any" in a_seek:
                    continue
                if b_have in a_seek:
                    continue
                else:
                    return False
            return True
        return compat(self, potential_partner) and compat(potential_partner, self)

    # def get_personal_member_pool(global_pool: list[])
        

def get_attr_have(member: discord.Member, roles: dict[str, dict[str, int]]):
    for k,v in roles.items():
        have_role = member.guild.get_role(v['have'])
        if have_role in member.roles:
            return k

def get_attr_seek(member: discord.Member, roles: dict[str, dict[str, int]]):
    seeking = []
    for k,v in roles.items():
        seek_role = member.guild.get_role(v['seek'])
        if seek_role in member.roles:
            seeking.append(k)

    return seeking or ["any"]