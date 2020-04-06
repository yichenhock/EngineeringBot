# python3 EngineeringBot/bot.py

import os
import glob
import random
import discord
import json
import datetime

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

# same path modules
import question

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='dad ')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='cribs', help='Link to Cam Cribs')
async def cribs(ctx):
    await ctx.send("Cam cribs: https://camcribs.com/")

@bot.command(name='hey', help='Wassup')
async def hey(ctx):
    await ctx.message.add_reaction("🍆")
    await ctx.send("What's up son")

#@bot.command(name='advice',help='')

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

@bot.command(name="bigcaps",help="BIGCAPS, like really big")
async def bigCaps(ctx, *args):
    await ctx.send("    ".join([txt2emoji(word) for word in args]))

@bot.command(name="nsfw",help="You know it :^)")
async def nsfw(ctx):
    images = []
    for filename in os.listdir(r"./EngineeringBot/nsfw"):
        if (filename.endswith(".jpg")) or (filename.endswith(".png")):
            images.append(filename)
    image = random.choice(images)
    file = discord.File("./EngineeringBot/nsfw/"+image, filename=image)
    embed = discord.Embed()
    embed.set_image(url="attachment://"+image)
    await ctx.send(file=file,embed=embed)

@bot.command(name="hmu",help="When you need someone to spice up your life, I'm here for it;)")
async def hmu(ctx):
    hmu_txt = []
    with open("./EngineeringBot/hmu.txt", "r") as a_file:
        for line in a_file:
            hmu_txt.append(line.strip())
    await ctx.message.add_reaction("💦")
    await ctx.send(random.choice(hmu_txt))

"""
@bot.command(name='potato',help='Hot Potato (not yet configured)')
async def potato(ctx): 
    pass
"""

bot.run(TOKEN)