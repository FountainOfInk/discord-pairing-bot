import discord
bot = discord.Bot()

ENABLED_GUILDS = [1097705595412414566]
ALLOWED_USERS = [1112153224196145192]

def is_which_role(member: discord.Member, roles: dict[str, dict[str, int]]):
    for k,v in roles.items():
        if member.guild.get_role(v['have']) in member.roles:
            return k


age_table = {
    "13": {'have': 1102378563547709470, 'seek': 1102431546146832434},
    "14": {'have': 1102378603175481447, 'seek': 1102431588895162399},
    "15": {'have': 1102378623446548540, 'seek': 1102431611120791602},
    "16": {'have': 1102378641024876595, 'seek': 1102431630578163762},
    "17": {'have': 1102378660448710708, 'seek': 1102431648282333285},
    "18": {'have': 1102378680283570246, 'seek': 1102431665940332685},
    "19": {'have': 1102378700323946526, 'seek': 1102431689290027059},
    "20": {'have': 1102378722226606241, 'seek': 1102431708462194750},
    "21": {'have': 1102378751335088129, 'seek': 1102431727747600384},
    # 22-25
    "22": {'have': 1102378769685164032, 'seek': 1102431752821157888},
    # 26+
    "26": {'have': 1102378806683115521, 'seek': 1102431778150559814},
    # any
    "any" : {'have': 1, 'seek': 1102431845246832691}
}

gender_table = {
    "male"  : {'have': 1102136394341679104, 'seek': 1102438467067191296},
    "female": {'have': 1102136573383954474, 'seek': 1102438530942259270},
    "nb"    : {'have': 1102141403385036881, 'seek': 1102438553843155004},
    "any"   : {'have': 1, 'seek': 1102438637351747624}
}

region_table = {
    "europe"        : {'have': 1102139562983161856, 'seek': 1102435439874424862},
    "northamerica"  : {'have': 1102139922749591593, 'seek': 1102435469414895666},
    "southamerica"  : {'have': 1102139866680135740, 'seek': 1102436807171375157},
    "asia"          : {'have': 1102139673259819038, 'seek': 1102435498552741929},
    "oceania"       : {'have': 1102139779627364473, 'seek': 1102435527501815890},
    "africa"        : {'have': 1102140014697132052, 'seek': 1102435591276212305},
    "any"           : {'have': 1, 'seek': 1102435709979213924}
}

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    

@bot.slash_command(guild_ids=ENABLED_GUILDS, name="among", description="among us!")
async def among(ctx: discord.ApplicationContext):
    await ctx.response.defer()
    if not ctx.author.id in ALLOWED_USERS:
        await ctx.respond("kys")
        return
    
    roles_added: str = "The roles you have been given are:\n"
    highest_bot_role = ctx.guild.get_member(bot.user.id).roles[-1]

    for role in ctx.guild.roles[highest_bot_role.position::-1]:
        try:
            await ctx.author.add_roles(role)
            roles_added += f"{role.name}\n"
            # await ctx.respond(f"Gave role {role.name}")
            # return
        except Exception as e:
            if isinstance(e, discord.errors.Forbidden):
                print(f"Unable to give role {role.name}, forbidden")
                continue
            else:
                await ctx.respond(e)
                raise e
            
    
    ctx.respond(roles_added)

@bot.slash_command(guild_ids=ENABLED_GUILDS, name="hjkl", description="among sus!")
async def vimkeys(ctx: discord.ApplicationContext):
    attributes = []
    for attribute in [age_table, region_table, gender_table]:
        attributes.append(is_which_role(ctx.author, attribute))
    await ctx.respond(f"Author {ctx.author} has attributes {attributes}")

bot.run("MTA5NzcwMzc2NzEzNjI4MDcyOQ.GzthWg.3eQq1T5VyZgnCoRDCP11_6rvfsgaMsqvYKriPM")
