from discord.ext import commands
import discord

from ShopItems import items

prefix = 'dad '

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name='shop')
    async def shop(self,ctx, item:str=None, amt:int=None):
        if item == None and amt == None: 
            shopDisplay = discord.Embed(title='Dyson Centre Store',
                            description='Yo, welcome kiddos! Come spend your <:stdc:696823503663530115> **Standard Credits**!')
            shopDisplay.add_field(name='Potato',value='Cost: 5',inline=True)
            await ctx.send('',embed=shopDisplay)
        else: 
            print(item)
            print(amt)

    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx):
        pass

def setup(bot):
    bot.add_cog(ShopCommands(bot))