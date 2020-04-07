# python3 bot.py

import os
import random
import discord
import json
import datetime
import time
import asyncio

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

# same path modules
import question

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PATH = ""

bot = commands.Bot(command_prefix='dad ',case_insensitive=True)

bot.remove_command('help')

data = {}

async def saveloop():
    while True:
        save_data()
        await asyncio.sleep(10)

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
    with open(PATH+'data.txt', 'w') as outfile:
        json.dump(data, outfile)

@bot.event
async def on_ready():
    global data
    print(f'{bot.user.name} has connected to Discord!')

    # checks if data file exist, if not, writes an empty dict to it
    if os.path.exists(PATH+"data.txt"):
        with open(PATH+"data.txt", "r") as json_file: 
            data = json.load(json_file)
    else:
        data = {}

    print(data)
    bot.loop.create_task(saveloop())

@bot.command(name='cribs', help='Link to Cam Cribs')
async def cribs(ctx):
    await ctx.send("Cam cribs: https://camcribs.com/")

@bot.command(name='lab',help='Do a lab for standard credit')
async def lab(ctx): 
    stdc = get_data(ctx.author.id, "stdc", default_val=0)

    add_data(ctx.author.id, "stdc", stdc+1)
    await ctx.send("You have collected `1` <:stdc:696823503663530115>!")
    print(stdc+1)

@bot.command(name='potato',help='Collect potato')
async def potato(ctx): 

    potatoes = get_data(ctx.author.id, "potatoes", default_val=0)

    add_data(ctx.author.id, "potatoes", potatoes+1)
    await ctx.send("You have collected `1` 🥔!")
    print(potatoes+1)

@bot.event
async def on_command_error(ctx, error):
    print("An error occured...")
    print(error)

if __name__ == '__main__':
    for extension in os.listdir(PATH+"cogs"):
        if (extension.endswith(".py")):
            try: 
                bot.load_extension("cogs."+extension.replace('.py', ''))
                print(f'Loaded extension {extension}.')
            except:
                print(f'Failed to load extension {extension}.')

bot.run(TOKEN)