import discord
import random
from discord.ext import commands
import os
import re

from constants import DATA_PATH

class ChatCommands(commands.Cog, name= "Chat"):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name='hey', help='Wassup')
    async def hey(self,ctx):
        await ctx.message.add_reaction("🍆")
        await ctx.send("What's up son")
    
    @commands.command(name = "I'm", help = "Uh huh", aliases=["im"])
    async def im(self, ctx, *msg): 
        await ctx.send("Hi "+ " ".join(msg) +" I'm dad")

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name} ~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.command(name="hmu",help="When you need someone to spice up your life, I'm here for it;)")
    async def hmu(self,ctx):
        hmu_txt = []
        with open(DATA_PATH+"hmu.txt", "r") as a_file:
            for line in a_file:
                hmu_txt.append(line.strip())
        await ctx.message.add_reaction("💦")
        await ctx.send(random.choice(hmu_txt))

def setup(bot):
    bot.add_cog(ChatCommands(bot))