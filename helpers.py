import discord
from discord.ext import commands
from extbot import Bot

ADMIN_PERM_INT = 8

class helpers(commands.Cog):
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="reload", description="reload some extension", default_member_permissions=discord.Permissions(ADMIN_PERM_INT))
    async def reloadCog(self, ctx: discord.ApplicationContext, module: str):
        await ctx.interaction.response.defer()
        try:
            self.bot.reload_extension(f"{module}")
            await ctx.respond(f"reloaded {module}")
        except Exception as e:
            await ctx.respond(e)


# You must have this function for `bot.load_extension` to call
def setup(bot):
    bot.add_cog(helpers(bot))
