from discord.ext import commands

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='shop')
    async def shop(self,ctx):
        pass

    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx):
        pass

def setup(bot):
    bot.add_cog(ShopCommands(bot))