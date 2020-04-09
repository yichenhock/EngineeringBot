from discord.ext import commands
import discord
import items
from data import add_data, get_data, save_data, get_player_item_amount, set_player_item_amount

prefix = 'dad '

sc_emoji = "<:stdc:696823503663530115>"

class ShopCommands(commands.Cog, name="Shop"):
    def __init__(self,bot):
        self.bot = bot
        items.import_items()
        
    @commands.command(name='shop')
    async def shop(self,ctx,*args):
        if len(args)==0:
            shop_disp = discord.Embed(title='Dyson Centre Store',
                            description='Yo, welcome kiddos! Come spend your {} **Standard Credits**!'.format(sc_emoji),
                            colour=discord.Color.gold())
            shop_desc = ''
            for i in items.items:
                if i.can_be_in_shop():
                    shop_desc += ('{} **{}** ─ {}{} \n{}\n\n'.format(i.emoji,i.name,sc_emoji,i.cost,i.description))

            shop_disp.add_field(name='Items',value=shop_desc,inline=False)
            msg = await ctx.send('',embed=shop_disp)
            await msg.add_reaction("◀️")
            await msg.add_reaction("▶️")
        else: 
            item = " ".join(args)
            i = items.get_by_name(item)
            if i is not None:
                if i.can_be_in_shop(): # If has shop_item in data
                    desc = '**COST: {} {}**'.format(sc_emoji,i.cost)
                else:
                    desc = "Can't be bought in the shop"
                    if i.has_value(): # If has cost in its data
                        desc = "Can't be bought in the shop\n**Value: {} {}**".format(sc_emoji,i.cost)
                item_disp = discord.Embed(title=i.emoji+" "+i.name,
                                    description=desc,
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

        i = items.get_by_name(item)
        if i is not None: 
            if i.can_be_in_shop(): # Will have to be replaced with a check to see if it is actually in the shop
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
                await ctx.send("Kid that's not in stock right now... and I say you shouldn't be wasting your money on random pidge-podge like this son.")
        else:
            await ctx.send("That item doesn't exist... have you been smoking the devil's lettuce again son?!")

    @commands.command(name='balance',aliases=['bal'])
    async def balance(self,ctx,member:discord.Member=None):
        if member == None:
            member = ctx.author

        sc = get_data(member.id, "sc", default_val=0)
        bal_disp = discord.Embed(title="{}'s balance".format(member.name),
                                description="**Standard Credit: {}`{}`**".format(sc_emoji,sc),
                                colour = discord.Color.dark_teal())
        await ctx.send('',embed=bal_disp)

    @commands.command(name='inventory',aliases = ['inv'])
    async def inv(self,ctx,member:discord.Member=None):
        if member == None:
            member = ctx.author

        sc = get_data(member.id, "sc", default_val=0)

        inv = get_data(member.id, "inv", default_val=0)
        inv_disp = discord.Embed(title="{}'s inventory".format(member.name),
                                description="Current balance: {}`{}`".format(sc_emoji,sc),
                                colour=discord.Color.dark_teal())
        inv_desc = ''
        for item, amt in inv.items():
            i=items.get_by_name(item)
            if amt >0:
                inv_desc += ('{} **{}** - {}'.format(items.get_by_name(item).emoji,item,amt)+'\n')
        
        inv_disp.add_field(name='Owned Items',value=inv_desc[0:len(inv_desc)-1],inline=False)
        await ctx.send('',embed=inv_disp)

    
    @commands.command(name='give',aliases=['gift'])
    async def give(self,ctx,member:discord.Member=None, *, item=None):
        
        inv = get_data(ctx.author.id, "inv", default_val=0)

        if member==None:
            await ctx.send("Kid, it goes like this:\n`dad gift <@user> <amount> <item name>`")

        elif member == ctx.author:
            await ctx.send("Lmao when you try to give yourself a present because you have no friends...")

        elif item.isdigit(): # Giving sc...
            amt = int(item)
            if get_data(ctx.author.id, "sc", default_val=0) < amt:
                await ctx.send("You don't have enough {} **Standard Credits** to give away!".format(sc_emoji))
            else:
                giver_after = get_data(ctx.author.id, "sc", default_val=0)-amt
                add_data(ctx.author.id, "sc",giver_after)
                reciever_after = get_data(member.id, "sc", default_val=0)+amt
                add_data(member.id, "sc",reciever_after)

                await ctx.send("You gave {} {} {}**Standard Credit(s)**, now you have {} and they've got {}.".format(member.display_name,amt,sc_emoji,giver_after,reciever_after))

        else:
            if item.split(' ', 1)[0].isdigit():
                amt = int(item.split(' ', 1)[0])
                item = item.split(' ', 1)[1]
            else:
                amt = 1
            print(amt, item)

            i = items.get_by_name(item)

            if i is not None: 
                giver_before = inv.get(i.name, 0)
                if inv[i.name] > 0:
                    if inv[i.name] >= amt:
                        giver_after = get_player_item_amount(ctx.author.id, i.name, default_val=0)-amt
                        set_player_item_amount(ctx.author.id, i.name,giver_after)
                        reciever_after = get_player_item_amount(member.id, i.name, default_val=0)+amt
                        set_player_item_amount(member.id, i.name,reciever_after)
                        await ctx.send("You gave {} {} {}**{}**(s), now you have {} and they've got {}.".format(member.display_name,amt,i.emoji,i.name,giver_after,reciever_after))

                    else:
                        await ctx.send("You don't have enough {}**{}**(s)!".format(i.emoji,i.name))

                else:
                    await ctx.send("Son, you don't own this item!")
                
            else:
                await ctx.send("The heck... that item doesn't exist!")

    @give.error
    async def on_message_error(self,ctx,error):
        await ctx.send("Kid, it goes like this:\n`dad gift <@user> <amount> <item name>`")

def setup(bot):
    bot.add_cog(ShopCommands(bot))