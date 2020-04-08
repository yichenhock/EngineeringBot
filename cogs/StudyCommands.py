from discord.ext import commands
from DataLogging import load_data, add_data, get_data, save_data

class StudyCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='lab',help="Do a lab for standard credit <:stdc:696823503663530115>.")
    async def lab(self,ctx): 
        stdc = get_data(ctx.author.id, "stdc", default_val=0)
        add_data(ctx.author.id, "stdc", stdc+1)
        await ctx.send("You have collected `1` <:stdc:696823503663530115>!")

    @commands.command(name='potato',help='Collect potato')
    async def potato(self,ctx): 
        potatoes = get_data(ctx.author.id, "potatoes", default_val=0)
        add_data(ctx.author.id, "potatoes", potatoes+1)
        await ctx.send("You have collected `1` 🥔!")
    
    @commands.command(name='trivia',help='Answer a question to get standard credit')
    async def trivia(self,ctx):
        user_level = get_data(ctx.author.id, "level", default_val=1)


def get_trivia_lecturer_message(user_level):
    """Get a message depending on who your lecturer currently is.
    Your lecturer changes depending on what level you are.
    """
    pass

def setup(bot):
    bot.add_cog(StudyCommands(bot))