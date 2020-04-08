from discord.ext import commands
import discord

prefix = "dad "

class HelpCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self,ctx,*cog):
        try: 
            if not cog: 
                """ Lists cogs """
                halp=discord.Embed(title='Command Category Listing and General Commands',
                               description='Use `'+ prefix +'help *category*` to find out more about them!\n(BTW, the Category Name Must Be in Title Case, Just Like this Sentence.)',
                               colour=discord.Color.gold())
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{}'.format(x)+'\n') #self.bot.cogs[x].__doc__
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='General Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
            else: 
                """Command listing within a cog."""
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    halp.add_field(name=c.name,value=c.help,inline=False)
                            found = True
                if not found:
                    """Reminds you if that cog doesn't exist."""
                    halp = discord.Embed(title='Bruh!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                else:
                    await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
        except:
            await ctx.send("Excuse me, I can't send embeds.")
        
        await ctx.send("Yes, you need help.")

def setup(bot):
    bot.add_cog(HelpCommands(bot))