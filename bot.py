# python3 bot.py

import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

# same path modules
from data import load_data, add_data, get_data, save_data
from parameters import PREFIX

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=PREFIX,case_insensitive=True)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    load_data(bot)

@bot.event
async def on_command_error(ctx, error):
    print("An error occured...")
    print(error)

if __name__ == '__main__':
    for extension in os.listdir("cogs"):
        if (extension.endswith(".py")):
            try: 
                bot.load_extension("cogs."+extension.replace('.py', ''))
                print(f'Loaded extension {extension}.')
            except:
                print(f'Failed to load extension {extension}.')

bot.run(TOKEN)