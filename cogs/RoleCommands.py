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
colleges1 = {
    "christ's": [754331432335442010,["christs"]], 
    "churchill": [754331585980923945],
    "clare" : [754331618553888868],
    "clare hall" : [754331638183493742],
    "corpus" : [754331674762018849,["corpus christi"]],
    "darwin" : [754331715081863178],
    "downing" : [754331739928789064],
    "emma" : [754331776318570498, ["emmanuel"]],
    "fitz" : [754331800276434964, ["fitzwilliam"]],
    "girton" : [754331825400184856],
    "homerton" : [754331849693724793],
    "hughes hall" : [754331869218209847, ["hughes"]],
    "jesus" : [754331902676041757],
    "lucy cav" : [754331930077429872, ["lucy","lucy cavendish"]],
    "magdalene" : [754331949803503623,["mag"]],
    "medwards" : [754331983332507768, ["murry edwards"]],
    "pembroke" : [754332013749862423, ["pem"]],
    "peterhouse" : [754332040677031976],
    "queens'" : [754332061996941382, ["queens"]],
    "robinson" : [754332095467356321],
    "selwyn" : [754332117575663746],
    "sidney sussex" : [754332137192292392,["sidney"]],
    "catz" : [754332166548095066,["st catz", "st catherine", "st catherine's"]],
    "st ed's" : [754332204229984346,["st edmunds", "st edmund's", "eddies", "st eds"]],
    "st john's" : [754332241550901318,["johns","john's","st johns"]],
    "trinity" : [754332265948905562],
    "trinity hall" : [754332291827761232,["tit hall"]],
    "wolfson" : [754332313076236288]
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
                    
                    role = get(message.guild.roles, name=role_name)

                    for r in message.author.roles: 
                        if r.name in colleges: 
                            await message.author.remove_roles(r)
                            await message.channel.send("You have been removed from **"+ r.name + "**.")

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