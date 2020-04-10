from discord.ext import commands
import parameters

class HealthCommands(commands.Cog, name="Health"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="wash")
    async def wash(self,ctx,*,item):
        await ctx.send("Nice. You washed your {}.".format(item))

def setup(bot):
    bot.add_cog(HealthCommands(bot))