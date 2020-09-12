from discord.ext import commands
from discord.utils import get
import discord
import random 
import os

# from constants import DATA_PATH
colleges = {
    "christ's": ["christs"], 
    "churchill": [],
    "clare" : [],
    "clare hall" : [],
    "corpus" : ["corpus christi"],
    "darwin" : [],
    "downing" : [],
    "emma" : ["emmanuel"],
    "fitz" : ["fitzwilliam"],
    "girton" : [],
    "homerton" : [],
    "hughes hall" : ["hughes"],
    "jesus" : [],
    "lucy cav" : ["lucy","lucy cavendish"],
    "magdalene" : ["mag"],
    "medwards" : ["murry edwards"],
    "pembroke" : ["pem"],
    "peterhouse" : [],
    "queens'" : ["queens"],
    "robinson" : [],
    "selwyn" : [],
    "sidney sussex" : ["sidney"],
    "catz" : ["st catz", "st catherine", "st catherine's"],
    "st ed's" : ["st edmunds", "st edmund's", "eddies", "st eds"],
    "st john's" : ["johns","john's","st johns"],
    "trinity" : [],
    "trinity hall" : ["tit hall"],
    "wolfson" : []
}

class RoleCommands(commands.Cog, name="Role"):
    def __init__(self,bot):
        self.bot = bot        
        self._respond = True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif (self._respond):
            
            if message.channel.id == 753064188036776036: # role-assignment channel
                role_name = ""
                for k, v in colleges.items():
                    if message.content == k: 
                        role_name = k
                    elif message.content in v: 
                        role_name = k

                if role_name != "": 
                    role_existing = False
                    role = get(message.guild.roles, name=role_name)

                    for r in message.author.roles: 
                        if r.name in colleges: 
                            if role_name != r.name: 
                                await message.author.remove_roles(r)
                                await message.channel.send("You have been removed from **"+ r.name + "**.")
                            else: 
                                await message.channel.send("You have already been assigned to **"+ r.name + "**.")
                                role_existing = True
                    if not role_existing: 
                        await message.author.add_roles(role)
                        await message.channel.send("You have been added to **"+ role_name + "**.")
                    # await message.author.add_roles(role)

                # print(message.content)
                # await message.channel.send("you sent something here!")
    


    # @commands.command(name="complex", help="Makes your sentence complex")
    # async def cmplx(self,ctx,*msg):
    #     await ctx.send(" ".join([word.replace("i", "j") for word in msg]))

def setup(bot):
    bot.add_cog(RoleCommands(bot))