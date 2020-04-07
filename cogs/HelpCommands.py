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
                halp=discord.Embed(title='Cog Listing and Uncatergorized Commands',
                               description='Use `'+ prefix +'help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Cogs',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='General Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
            else: 
                pass
        except:
            await ctx.send("Yes, you need help.")

def setup(bot):
    bot.add_cog(HelpCommands(bot))