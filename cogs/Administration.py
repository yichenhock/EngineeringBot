from discord.ext import commands

class Administration(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def shutdown(self,ctx):
        if ctx.message.author.id == 501077051017789451: #replace OWNERID with your user id
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