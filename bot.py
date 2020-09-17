# python3 bot.py

import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

# same path modules
from data import load_data, add_data, get_data, save_data
import items
import lecturers
from constants import PREFIX

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=PREFIX,case_insensitive=True)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    print("An error occured...")
    print(error)

@bot.event
async def on_member_join(member): 
    channel = bot.get_channel(695042957757382737)
    await channel.send(f"Welcome {member.mention}, I'm **Engi-Dad**. Check out #info-and-rules and give yourself a role in #role-assignment by typing the name of your college! \nI can do lots of cool stuff kid, go to #dad-bot to mess around with my commands. Dad out!")
    #await channel.send(f"Welcome {member.mention}, I'm **Engi-Dad**. Check out #info-and-rules and give yourself a role in #role-assignment by typing the name of your college! Type `dad help` more commands. ")

def initialise_data():
    load_data(bot)
    items.import_items()
    lecturers.import_lecturers()

initialise_data()

if __name__ == '__main__':
    for extension in os.listdir("cogs"):
        if (extension.endswith(".py")):
            try: 
                bot.load_extension("cogs."+extension.replace('.py', ''))
                print(f'Loaded extension {extension}.')
            except Exception as e:
                print(e)
                print(f'Failed to load extension {extension}.')

bot.run(TOKEN)