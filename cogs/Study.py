from discord.ext import commands

class StudyCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='lab',help="Do a lab for standard credit <:stdc:696823503663530115>.")
    async def lab(self,ctx): 
        stdc = get_data(ctx.author.id, "stdc", default_val=0)
        add_data(ctx.author.id, "stdc", stdc+1)
        await ctx.send("You have collected `1` <:stdc:696823503663530115>!")

def setup(bot):
    bot.add_cog(StudyCommands(bot))