from discord.ext import commands
import discord
import random 
import os

PATH = ""

def txt2emoji(txt): 
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    txt_chara = list(txt)
    for index in range(len(txt_chara)):
        if txt_chara[index] in alphabet:
            txt_chara[index] = ":regional_indicator_"+txt_chara[index]+":"
        elif txt_chara[index] == "B":
            txt_chara[index] = ":b:"
        elif txt_chara[index] == "!":
            txt_chara[index] = ":exclamation:"
        elif txt_chara[index] == "?":
            txt_chara[index] = ":question:"
    return "".join(txt_chara)

class MiscCommands(commands.Cog, name="Misc"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="complex", help="Makes your sentence complex")
    async def cmplx(self,ctx,*msg):
        await ctx.send(" ".join([word.replace("i", "j") for word in msg]))

    @commands.command(name="bigcaps",help="BIGCAPS, like really big")
    async def bigCaps(self,ctx, *args):
        await ctx.send("    ".join([txt2emoji(word) for word in args]))

    @commands.command(name="nsfw",help="You know it :^)")
    async def nsfw(self,ctx):
        images = []
        for filename in os.listdir(PATH+"nsfw"):
            if (filename.endswith(".jpg")) or (filename.endswith(".png")):
                images.append(filename)
        image = random.choice(images)
        file = discord.File("./EngineeringBot/nsfw/"+image, filename=image)
        embed = discord.Embed()
        embed.set_image(url="attachment://"+image)
        await ctx.send(file=file,embed=embed)

def setup(bot):
    bot.add_cog(MiscCommands(bot))