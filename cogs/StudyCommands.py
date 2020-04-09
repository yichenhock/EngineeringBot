from discord.ext import commands
from data import add_data, get_data, save_data
import discord
import random

sc_emoji = "<:stdc:696823503663530115>"

class StudyCommands(commands.Cog,name="Study"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='lab',help="Do a lab for {}**Standard Credit**.".format(sc_emoji))
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lab(self,ctx): 
        stdc = get_data(ctx.author.id, "sc", default_val=0)
        add_sc = random.randint(1,10)
        add_data(ctx.author.id, "sc", stdc+add_sc)
        await ctx.send("You did a lab for {}`{}`!".format(sc_emoji,add_sc))
    
    @commands.command(name='trivia',help='Answer a question to get standard credit')
    async def trivia(self,ctx):
        user_level = get_data(ctx.author.id, "level", default_val=1)

    @lab.error
    async def on_message_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            desc = "Your lab hasn't begun yet! Your demonstrator will be here in `{:.2f}` seconds".format(error.retry_after)
            msg = discord.Embed(description=desc,
                                colour=discord.Color.red())
            await ctx.send('',embed=msg)


def get_trivia_lecturer_message(user_level):
    """Get a message depending on who your lecturer currently is.
    Your lecturer changes depending on what level you are.
    """
    pass

def setup(bot):
    bot.add_cog(StudyCommands(bot))