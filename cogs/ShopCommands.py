from discord.ext import commands
import discord
import ShopItems
from DataLogging import load_data, add_data, get_data, save_data

prefix = 'dad '

sc = "<:stdc:696823503663530115>"

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot
        ShopItems.import_items()

    @commands.command(name='shop')
    async def shop(self,ctx, item:str=None):
        if item == None: 
            shop_disp = discord.Embed(title='Dyson Centre Store',
                            description='Yo, welcome kiddos! Come spend your {} **Standard Credits**!'.format(sc),
                            colour=discord.Color.gold())


            shop_desc = ''
            for i in ShopItems.items:
                shop_desc += ('{} **{}** ─ {}{} \n{}\n\n'.format(i.emoji,i.name,sc,i.cost,i.description))

            shop_disp.add_field(name='Items',value=shop_desc,inline=False)
            await ctx.send('',embed=shop_disp)
        else: 
            i = ShopItems.get_by_name(item)
            if i is not None:
                item_disp = discord.Embed(title=i.emoji+" "+i.name,
                                    description='**COST: {} {}**'.format(sc,i.cost),
                                    colour=discord.Colour.gold())
                item_disp.add_field(name='Description',value=i.description,inline=False)
                await ctx.send('',embed=item_disp)
            else:
                await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")
    
    @commands.command(name='buy')
    async def buy(self,ctx,*args):
        
        if args[-1].isdigit():
            amt = args[-1] 
            item = " ".join(args[:-1])
        else:
            item = " ".join(args)
            amt = 1

        i = ShopItems.get_by_name(item)
        if i is not None: 
            stdc = get_data(ctx.author.id, "sc", default_val=0)
            if stdc >= i.cost*amt:
                sale_disp = discord.Embed(colour=discord.Color.gold())
                sale_disp.set_author(name='Successful purchase',url='',icon_url=ctx.author.avatar_url)
                sale_disp.add_field(name='\u200b',value='You bought {} **{}** and paid {}`{}`'.format(amt,i.name,sc,i.cost),inline=False)
                await ctx.send('',embed=sale_disp)

                add_data(ctx.author.id, i.name, stdc - i.cost*amt)

            else:
                await ctx.send("You don't have enough money for this son, go do your work for {} **Standard Credits**.".format(sc))
        else:
            await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")


    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx):
        
        pass

def setup(bot):
    bot.add_cog(ShopCommands(bot))