from discord.ext import commands
import parameters

class HealthCommands(commands.Cog, name="Health"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="washhands",aliases=["wash"])
    async def washHands(self,ctx):
        await ctx.send("Nice. You washed your hands.")

def setup(bot):
    bot.add_cog(HealthCommands(bot))