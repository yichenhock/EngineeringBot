from discord.ext import commands
import constants

class Administration(commands.Cog, name="Admin"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="shutdown",help="Shuts down all instances of servers running the bot.")
    async def shutdown(self,ctx):
        if ctx.message.author.id in constants.adminID: #replace OWNERID with your user id
            print("shutdown")
            try:
                await self.bot.logout()
            except:
                print("EnvironmentError")
                self.bot.clear()
        else:
            await ctx.send("You do not own this bot!")

def setup(bot):
    bot.add_cog(Administration(bot))