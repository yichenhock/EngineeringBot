from discord.ext import commands
import discord
from constants import PREFIX

class HelpCommands(commands.Cog,name="Help"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self,ctx,*cog):
        try:
            if not cog: 
                """ Lists cogs """
                halp=discord.Embed(title='Command Category Listing and General Commands',
                                description='Use `{}help *category*` to find out more about them!'.format(PREFIX),
                                colour=discord.Color.red())
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{}\n'.format(x)) #self.bot.cogs[x].__doc__
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}\n'.format(y.name,y.help))
                print(cmds_desc)
                if cmds_desc !='':
                    halp.add_field(name='General Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send(embed=halp)
            else: 
                """Command listing within a cog."""
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x.lower() == y.lower():
                            halp=discord.Embed(title=x+' Command Listing',
                                            description=self.bot.cogs[x].__doc__,
                                            colour=discord.Color.red())
                            for c in self.bot.get_cog(x).get_commands():
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

def setup(bot):
    bot.add_cog(HelpCommands(bot))