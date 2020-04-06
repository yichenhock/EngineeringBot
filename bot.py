# bot.py
import os
import random
import discord
import json
import datetime

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

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
    await ctx.send("  ".join([txt2emoji(word) for word in args]))

@bot.command(name='potato',help='Hot Potato (not yet configured)')
async def potato(ctx): 
    pass

bot.run(TOKEN)