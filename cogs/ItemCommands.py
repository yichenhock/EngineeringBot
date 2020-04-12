from discord.ext import commands
import discord
import os
from constants import PATH
import items


class ItemCommands(commands.Cog, name="Items"):
    def __init__(self,bot):
        self.bot = bot
        # All functions here must have ctx as an input parameter.
        self.item_use_func = {
            "Kit Kat Chunky": self.use_kit_kat,
            "Penny": self.use_penny,
        }

    @commands.command(name="use",help="Use an item")
    async def use(self,ctx, *, item_name):
        item = items.get_by_name(item_name)
        if item is not None:
            if item.name in self.item_use_func:
                await self.item_use_func[item.name](ctx)

    async def use_kit_kat(self, ctx):
        ctx.send("Who do you want to throw your Kit Kat Chunky to?")
        ctx.send("Not currently implemented") # Use wait_for("message", check, timeout = 60) where check is a check function (look up the API)

    async def use_penny(self, ctx):
        ctx.send("Not currently implemented")

def setup(bot):
    bot.add_cog(ItemCommands(bot))