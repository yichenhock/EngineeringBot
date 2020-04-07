from discord.ext import commands
import os
import random 
import re

PATH = ""

class SettingsCommands(commands.Cog, name="Settings"):
    def __init__(self,bot):
        self.bot = bot        
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
    
    @commands.command(name="toggle",help="Turn on/off buzzword responses")
    async def toggle(self,ctx):
        if self._respond:
            await ctx.send("Okay then, bye.")
            self._respond = False
        else: 
            await ctx.send("I'm back kiddo.")
            self._respond = True

def setup(bot):
    bot.add_cog(SettingsCommands(bot))