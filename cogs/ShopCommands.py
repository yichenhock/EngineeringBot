import asyncio
import random
from math import ceil
from time import time

import discord
from discord.ext import commands

import items
import tips
from constants import PREFIX, SC_EMOJI
from data import add_data, get_data, save_data
from paginator import Paginator

SHOP_SIZE = 10

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot
        

        self.stock = None
        stock_names = get_data("shop", "items", default_val = None)
        if stock_names:
            self.stock = [items.get_by_name(name) for name in stock_names]
        else:
            self.change_stock()
        
        bot.loop.create_task(self.updateloop())

    async def updateloop(self):
        while True:
            last_update_day = seconds_to_day(get_data("shop", "last_stock_change", default_val=0))
            if seconds_to_day(time()) != last_update_day:
                self.change_stock()
            await asyncio.sleep(60)

    def change_stock(self):
        add_data("shop", "last_stock_change", time())
        # Get all possible items
        shop_items = [] 
        for i in items.items:
            if i.can_be_in_shop():
                shop_items.append(i)

        # Pick a subset
        self.stock = random.sample(shop_items, min(SHOP_SIZE,len(shop_items)))  
        self.stock = sorted(self.stock, key=lambda x:x.name)
        stock_names = [item.name for item in self.stock]
        add_data("shop", "items", stock_names)

    async def on_item_reacted(self, ctx, item):
        await self.buy_item(ctx, item, 1)

    # @commands.command(name='testing')
    # async def testing(self,ctx):
    #     pages = [discord.Embed(title="Page 1"),
    #             discord.Embed(title="Page 2"),
    #             discord.Embed(title="Page 3"),
    #             discord.Embed(title="Page 4")
    #             ]
    #     menu = Paginator(self.bot,ctx,pages,timeout=60)
    #     await menu.run()


    @commands.command(name='shop',help="See what's in the Dyson Centre store")
    async def shop(self,ctx,*args):
        if len(args)==0:
            pages = []

            # Getting the items that are in the shop
            shop_items = []
            shop_items = self.stock

            shop_items = sorted(shop_items, key=lambda x:x.name)

            # Putting descriptions together
            n = 5
            strings = []
            string = ''
            page_items = []
            current_page_items = []
            for i, item in enumerate(shop_items):
                current_page_items.append(item)
                string = string+ item.get_shop_string()
                if i % n == n-1:
                    strings.append(string)
                    string = ""
                    page_items.append(current_page_items)
                    current_page_items = []

            if string:
                strings.append(string)
                page_items.append(current_page_items)

            for s in strings:
                if pages == []:
                    h, m, _ = get_time_to_shop_refresh()
                    reset_message = f"*The store will change its stock in {h:02}h {m:02}m*"
                    pages.append(discord.Embed(title='Dyson Centre Store',
                                description="Yo, welcome kiddos! Come spend your {} **Standard Credits**!\nUse the **arrow reactors** below to browse the store.\n**Click on an emoji** to buy one of that item, or use\n`dad buy <item> <amount>`\n\n".format(SC_EMOJI)+reset_message,
                                colour=discord.Color.gold()))
                else:
                    pages.append(discord.Embed(colour=discord.Color.gold()))
                pages[-1].add_field(name='Items',value=s,inline=False)

            menu = Paginator(self.bot,ctx,pages, page_items, self, timeout=60)
            await menu.run()

        else: 
            item = " ".join(args)
            i = items.get_by_name(item)
            if i is not None:
                if i.can_be_in_shop(): # If has shop_item in data
                    desc = '**COST: {} {}**'.format(SC_EMOJI,i.cost)
                    if not i in self.stock:
                        desc = desc + "\n*Currently not in stock*"
                else:
                    desc = "*Can't be bought in the shop*"
                    if i.has_value(): # If has cost in its data
                        desc = "**Value: {} {}**\n*Can't be bought in the shop*".format(SC_EMOJI,i.cost)
                item_disp = discord.Embed(title=i.emoji+" "+i.name,
                                    description=desc,
                                    colour=discord.Colour.gold())
                item_disp.add_field(name='Description',value=i.description,inline=False)
                if i.is_booster():
                    text = "_Each gives a_ {:.1f}%  _bonus to_ **{}**_, up to a maximum of_ {}%.".format(i.boost_bonus*100, i.boost_category.title(), i.boost_max_bonus*100)
                    item_disp.add_field(name='Booster',value=text,inline=False)

                    
                await ctx.send('',embed=item_disp)
            else:
                await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")


    @commands.command(name='buy',help="Buy an item from the store.")
    async def buy(self,ctx,*,in_string=None):
        
        if in_string == None:
            await ctx.send("What do you wanna buy kiddo?")

        name, amt = get_name_and_amount(in_string)

        i = items.get_by_name(name)
        await self.buy_item(ctx, i, amt)
        tip = tips.get_random_tip(0.4)
        if tip:
            await ctx.send(tip)


    @commands.command(name='balance',aliases=['bal'],help="Check the standard credits that you or someone else owns.")
    async def balance(self,ctx,member:discord.Member=None):
        if member == None:
            member = ctx.author

        tip = tips.get_random_tip(0.2)
        if tip:
            await ctx.send(tip)

        sc = get_data(member.id, "sc", default_val=0)
        bal_disp = discord.Embed(title="{}'s balance".format(member.name),
                                description="**Standard Credit: {}`{}`**".format(SC_EMOJI,sc),
                                colour = discord.Color.dark_teal())
        await ctx.send('',embed=bal_disp)


    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx,member:discord.Member=None):
        if member == None:
            member = ctx.author

        tip = tips.get_random_tip(0.2)
        if tip:
            await ctx.send(tip)

        sc = get_data(member.id, "sc", default_val=0)

        inv = get_data(member.id, "inv", default_val={})

        inv_disp = discord.Embed(title="{}'s inventory".format(member.name),
                                description="Current balance: {}`{}`".format(SC_EMOJI,sc),
                                colour=discord.Color.dark_teal())
        inv_desc = ''
        for item, amt in inv.items():
            if amt >0:
                inv_desc += ('{} **{}** - {}'.format(items.get_by_name(item).emoji,item,amt)+'\n')
        
        if inv_desc == '':
            inv_desc = "{} doesn't own anything! ".format(member.name)

        inv_disp.add_field(name='Owned Items',value=inv_desc[0:len(inv_desc)-1],inline=False)
        await ctx.send('',embed=inv_disp)

    
    @commands.command(name='give',aliases=['gift'])
    async def give(self,ctx,member:discord.Member=None, *, in_string=None):

        inv = get_data(ctx.author.id, "inv", default_val={})

        if member==None:
            await ctx.send("Kid, it goes like this:\n`dad give <@user> <amount> <item name>`")

        elif member == ctx.author:
            await ctx.send("Lmao when you try to give yourself a present because you have no friends...")

        elif in_string.isdigit(): # Giving sc...
            amt = int(in_string)
            if get_data(ctx.author.id, "sc", default_val=0) < amt:
                await ctx.send("You don't have enough {} **Standard Credits** to give away!".format(SC_EMOJI))
            else:
                giver_after = get_data(ctx.author.id, "sc", default_val=0)-amt
                add_data(ctx.author.id, "sc",giver_after)
                reciever_after = get_data(member.id, "sc", default_val=0)+amt
                add_data(member.id, "sc",reciever_after)

                await ctx.send("You gave {} {} {}**Standard Credit(s)**, now you have {} and they've got {}.".format(member.display_name,amt,SC_EMOJI,giver_after,reciever_after))

        else:
            name, amt = get_name_and_amount(in_string)

            i = items.get_by_name(name)

            if i is not None: 
                giver_before = inv.get(i.name, 0)
                if giver_before > 0:
                    if giver_before >= amt:
                        giver_after = get_data(ctx.author.id, "inv", i.name, default_val=0)-amt
                        add_data(ctx.author.id, "inv", i.name, giver_after)
                        reciever_after = get_data(member.id, "inv", i.name, default_val=0)+amt
                        add_data(member.id, "inv", i.name, reciever_after)
                        await ctx.send("You gave {} {} {}**{}**(s), now you have {} and they've got {}.".format(member.display_name,amt,i.emoji,i.name,giver_after,reciever_after))

                    else:
                        await ctx.send("You don't have enough {}**{}**(s)!".format(i.emoji,i.name))

                else:
                    await ctx.send("Son, you don't own this item!")
                
            else:
                await ctx.send("The heck... that item doesn't exist!")


    async def buy_item(self, ctx, item, amt):
        if item is not None: 
            if item.can_be_in_shop():
                if item in self.stock:
                    sc = get_data(ctx.author.id, "sc", default_val=0)
                    if sc >= item.cost*amt:
                        sale_disp = discord.Embed(colour=discord.Color.gold())
                        sale_disp.set_author(name='Successful purchase',url='',icon_url=ctx.author.avatar_url)
                        sale_disp.add_field(name='\u200b',value='You bought {} **{}**(s) and paid {}`{}`'.format(amt,item.name,SC_EMOJI,item.cost*amt),inline=False)
                        await ctx.send('',embed=sale_disp)

                        add_data(ctx.author.id, "inv", item.name,get_data(ctx.author.id, "inv", item.name, default_val=0)+amt)
                        add_data(ctx.author.id, "sc", sc - item.cost*amt)

                    else:
                        await ctx.send("You don't have enough money for this son, go do your work for {} **Standard Credits**.".format(SC_EMOJI))
                else:
                    await ctx.send("Kid that's not in stock right now... and I say you shouldn't be wasting your money on random pidge-podge like this son.")
            else:
                await ctx.send("Kid, the Dyson Centre store doesn't even sell this. Is that even legal?")
        else:
            await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")

    @give.error
    async def on_message_error(self,ctx,error):
        await ctx.send("Kid, it goes like this:\n`dad give <@user> <amount> <item name>`")


def setup(bot):
    bot.add_cog(ShopCommands(bot))


def get_name_and_amount(string):
    words = string.split()
    if words[0].isdigit():
        amt = int(words[0])
        name = " ".join(words[1:])
    elif words[-1].isdigit():
        amt = int(words[-1])
        name = " ".join(words[:-1])
    else:
        amt = 1
        name = " ".join(words)
    return name, amt

def seconds_to_day(seconds):
    return seconds // (24 * 60 * 60)

def seconds_to_hms(seconds):
    seconds = int(seconds)
    h = seconds//(60*60)
    m = (seconds-h*60*60)//60
    s = seconds-(h*60*60)-(m*60)
    return h, m, s

def get_time_to_shop_refresh():
    seconds = time() % (24 * 60 * 60) # time since start of day
    seconds = (24 * 60 * 60) - seconds # time to end of day
    return seconds_to_hms(seconds)
