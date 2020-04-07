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
from DataLogging import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='dad ',case_insensitive=True)

bot.remove_command('help')

data = {}


# def add_data(player_id, data_key, value):
#     """Add or insert a data entry into a player's data."""
#     player_id = str(player_id)
#     data_key = str(data_key)

#     if not player_id in data:
#         data[player_id] = {}
#     data[player_id][data_key] = value
#     print(data)

# def get_data(player_id, data_key, default_val=None):
#     """Get a data entry from a specific player."""
#     player_id = str(player_id)
#     data_key = str(data_key)

#     if not player_id in data:
#         return default_val
#     return data[player_id].get(data_key, default_val)

# def save_data():
#     with open(PATH+'data.txt', 'w') as outfile:
#         json.dump(data, outfile, sort_keys=True, indent=4)

@bot.event
async def on_ready():
    global data
    print(f'{bot.user.name} has connected to Discord!')
    DataLogging.load_data(bot)


@bot.command(name='cribs', help='Link to Cam Cribs')
async def cribs(ctx):
    await ctx.send("Cam cribs: https://camcribs.com/")


@bot.command(name='potato',help='Collect potato')
async def potato(ctx): 
    potatoes = get_data(ctx.author.id, "potatoes", default_val=0)
    add_data(ctx.author.id, "potatoes", potatoes+1)
    await ctx.send("You have collected `1` 🥔!")

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