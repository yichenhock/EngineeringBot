from discord.ext import commands
import discord
import parameters
import ShopItems

prefix = 'dad '

sc = parameters.sc

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot
        ShopItems.import_items()

    @commands.command(name='shop')
    async def shop(self,ctx, item:str=None, amt:int=None):
        if item == None and amt == None: 
            shopDisplay = discord.Embed(title='Dyson Centre Store',
                            description='Yo, welcome kiddos! Come spend your {} **Standard Credits**!'.format(sc))

            shop_desc = ''
            for item in ShopItems.items:
                shop_desc += ('{} **{}** ─ {}} {} \n{}\n\n'.format(item.emoji,item.name,sc,item.cost,item.description))

            shopDisplay.add_field(name='Items',value=shop_desc,inline=False)
            await ctx.send('',embed=shopDisplay)
        else: 
            print(item)
            print(amt)

    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx):
        pass

def setup(bot):
    bot.add_cog(ShopCommands(bot))