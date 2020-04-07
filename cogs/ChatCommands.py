import discord
import random
from discord.ext import commands
import os
import re

PATH = ""

class ChatCommands(commands.Cog, name= "Just here to chat"):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None
        self._respond = True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif (self._respond):
            """ Send random responses to buzzwords """
            for filename in os.listdir(PATH+"RandomResponses"):
                r = []
                f = os.path.splitext(filename)[0]
                words = re.findall(r'\w+', message.content)
                for word in words: 
                    if word.lower() == f:
                        with open(PATH+"RandomResponses/"+filename, "r") as a_file:
                            for line in a_file:
                                r.append(line.strip())
                        await message.channel.send(random.choice(r))
        await self.bot.process_commands(message)

    @commands.command(name='turnoff', aliases=['fuckoff','goaway','leave','bye','shutup'],help="Turn off reponses to buzzwords")
    async def off(self,ctx):
        if (self._respond):
            await ctx.send("Okay then, bye.")
            self._respond = False
    
    @commands.command(name='comeback', aliases=['dontleaveme','iwantuback'],help="Turn on reponses to buzzwords")
    async def on(self,ctx):
        if self._respond == False: 
            await ctx.send("I'm back kiddo.")
            self._respond = True

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
        with open(PATH+"hmu.txt", "r") as a_file:
            for line in a_file:
                hmu_txt.append(line.strip())
        await ctx.message.add_reaction("💦")
        await ctx.send(random.choice(hmu_txt))

def setup(bot):
    bot.add_cog(ChatCommands(bot))