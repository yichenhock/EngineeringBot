from discord.ext import commands
from data import add_data, get_data, save_data, get_lecturer_from_level
from constants import XP_INCREASE_PER_LEVEL, XP_TO_LEVEL_UP
import discord
import random
import tips

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

        string = "You did a lab for {}`{}`!".format(sc_emoji,add_sc)
        tip = tips.get_random_tip(0.4)
        if tip:
            string = tip + "\n\n" + string
        await ctx.send(string)
        await give_xp(ctx, ctx.author.id, 3)
    
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

    @commands.command(name='cribs', help='Link to Cam Cribs')
    async def cribs(self,ctx):
        await ctx.send("Cam cribs: https://camcribs.com/")


async def give_xp(ctx, p_id, amount):
    level = int(get_data(p_id, "level", default_val=0))
    current_xp = int(get_data(p_id, "xp", default_val=0))
    new_xp = current_xp + amount
    xp_required = XP_TO_LEVEL_UP + XP_INCREASE_PER_LEVEL * level
    while new_xp >= xp_required:
        new_xp -= xp_required
        level += 1
        xp_required = XP_TO_LEVEL_UP + XP_INCREASE_PER_LEVEL * level
        await ctx.send(":tada:  **{} has Levelled Up to Level {}**  :tada:\n".format(ctx.author.mention, level))
        await ctx.send("> Your new lecturer is {}".format(get_lecturer_from_level(level)["name"]))
        await ctx.send("\n*Note: The level system is currently a WIP and your level will be reset when it is complete.*")
    add_data(p_id, "level", level)
    add_data(p_id, "xp", new_xp)

def get_trivia_lecturer_message(user_level):
    """Get a message depending on who your lecturer currently is.
    Your lecturer changes depending on what level you are.
    """
    pass

def setup(bot):
    bot.add_cog(StudyCommands(bot))
