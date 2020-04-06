# python3 EngineeringBot/bot.py

import os
import glob
import random
import discord
import json
import datetime
import time
import re

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

# same path modules
import question

path = "./EngineeringBot/"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='dad ',case_insensitive=True)

data = {}

def add_data(player_id, data_key, value):
    """Add or insert a data entry into a player's data."""
    if not player_id in data:
        data[player_id] = {}
    data[player_id][data_key] = value

def get_data(player_id, data_key, default_val=None):
    """Get a data entry from a specific player."""
    if not player_id in data:
        return default_val
    return data[player_id].get(data_key, default_val)

def save_data():
    with open(path+'data.txt', 'w') as outfile:
        json.dump(data, outfile)

@bot.event
async def on_ready():
    global data
    print(f'{bot.user.name} has connected to Discord!')

    # Load data
    if os.path.exists(path):
        with open(path+"data.txt", "r") as json_file: 
            data = json.load(json_file)
    else:
        data = {}
    print(data)

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

@bot.command(name="i'm", help="Uh huh")
async def im(ctx, *msg):
    await ctx.send("Hi "+ " ".join(msg) +" I'm dad")

@bot.command(name="complex", help="Makes your sentence complex")
async def cmplx(ctx,*msg):
    await ctx.send(" ".join([word.replace("i", "j") for word in msg]))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    else:
        for filename in os.listdir(path+"random_responses"):
            r = []
            f = os.path.splitext(filename)[0]
            words = re.findall(r'\w+', message.content)
            for word in words: 
                if word.lower() == f:
                    with open(path+"random_responses/"+filename, "r") as a_file:
                        for line in a_file:
                            r.append(line.strip())
                    await message.channel.send(random.choice(r))
                
    await bot.process_commands(message)

@bot.command(name='lab',help='Do a lab for standard credit')
async def lab(ctx): 

    stdc = get_data(ctx.author.id, "stdc", default_val=0)
    add_data(ctx.author.id, "stdc", stdc+1)

    save_data()

    await ctx.send("You have collected `1` <:stdc:696823503663530115>!")

@bot.command(name='potato',help='Collect potato')
async def potato(ctx): 

    potatoes = get_data(ctx.author.id, "potatoes", default_val=0)
    add_data(ctx.author.id, "potatoes", potatoes+1)

    save_data()

    await ctx.send("You have collected `1` 🥔!")

bot.run(TOKEN)