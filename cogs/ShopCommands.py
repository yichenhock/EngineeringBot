from discord.ext import commands
import discord
import ShopItems
from DataLogging import load_data, add_data, get_data, save_data, get_inv

prefix = 'dad '

sc_emoji = "<:stdc:696823503663530115>"

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot
        ShopItems.import_items()

    @commands.command(name='shop')
    async def shop(self,ctx,*args):
        if len(args)==0:
            shop_disp = discord.Embed(title='Dyson Centre Store',
                            description='Yo, welcome kiddos! Come spend your {} **Standard Credits**!'.format(sc_emoji),
                            colour=discord.Color.gold())
            shop_desc = ''
            for i in ShopItems.items:
                shop_desc += ('{} **{}** ─ {}{} \n{}\n\n'.format(i.emoji,i.name,sc_emoji,i.cost,i.description))

            shop_disp.add_field(name='Items',value=shop_desc,inline=False)
            await ctx.send('',embed=shop_disp)
        else: 
            item = " ".join(args)
            i = ShopItems.get_by_name(item)
            if i is not None:
                item_disp = discord.Embed(title=i.emoji+" "+i.name,
                                    description='**COST: {} {}**'.format(sc_emoji,i.cost),
                                    colour=discord.Colour.gold())
                item_disp.add_field(name='Description',value=i.description,inline=False)
                await ctx.send('',embed=item_disp)
            else:
                await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")
    
    @commands.command(name='buy')
    async def buy(self,ctx,*args):
        
        if len(args)==0:
            await ctx.send("What do you wanna buy kiddo?")

        if args[-1].isdigit():
            amt = int(args[-1])
            item = " ".join(args[:-1])
        else:
            item = " ".join(args)
            amt = 1

        i = ShopItems.get_by_name(item)
        if i is not None: 
            sc = get_data(ctx.author.id, "sc", default_val=0)
            if sc >= i.cost*amt:
                sale_disp = discord.Embed(colour=discord.Color.gold())
                sale_disp.set_author(name='Successful purchase',url='',icon_url=ctx.author.avatar_url)
                sale_disp.add_field(name='\u200b',value='You bought {} **{}** and paid {}`{}`'.format(amt,i.name,sc_emoji,i.cost*amt),inline=False)
                await ctx.send('',embed=sale_disp)

                add_data(ctx.author.id, i.name,get_data(ctx.author.id, i.name, default_val=0)+1)
                add_data(ctx.author.id, "sc", sc - i.cost*amt)

            else:
                await ctx.send("You don't have enough money for this son, go do your work for {} **Standard Credits**.".format(sc_emoji))
        else:
            await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")

    @commands.command(name='balance',aliases=['bal'])
    async def balance(self,ctx):
        sc = get_data(ctx.author.id, "sc", default_val=0)
        bal_disp = discord.Embed(title="{}'s balance".format(ctx.author.name),
                                description="**Standard Credit: {}`{}`**".format(sc_emoji,sc),
                                colour = discord.Color.dark_teal())
        await ctx.send('',embed=bal_disp)

    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx):
        sc = get_data(ctx.author.id, "sc", default_val=0)

        inv = get_inv(ctx.author.id, default_val=0)
        inv_disp = discord.Embed(title="{}'s inventory".format(ctx.author.name),
                                description="Current balance: {}`{}`".format(sc_emoji,sc),
                                colour=discord.Color.dark_teal())
        inv_desc = ''
        for item, amt in inv.items():
            i=ShopItems.get_by_name(item)
            if i is not None:
                inv_desc += ('{} **{}** - {}'.format(ShopItems.get_by_name(item).emoji,item,amt)+'\n')
        
        inv_disp.add_field(name='Owned Items',value=inv_desc[0:len(inv_desc)-2],inline=False)
        await ctx.send('',embed=inv_disp)

def setup(bot):
    bot.add_cog(ShopCommands(bot))