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
# from discord.ext import buttons
from libneko import pag
from dotenv import load_dotenv

# same path modules
import question
from data import load_data, add_data, get_data, save_data

import parameters
PATH = parameters.PATH

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


"""
class MyPaginator(buttons.Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @buttons.button(emoji='\u23FA')
    async def record_button(self, ctx, member):
        await ctx.send('This button sends a silly message! But could be programmed to do much more.')

    @buttons.button(emoji='my_custom_emoji:1234567890')
    async def silly_button(self, ctx, member):
        await ctx.send('Beep boop...')
"""
bot = commands.Bot(command_prefix='dad ',case_insensitive=True)

bot.remove_command('help')

"""
@bot.command()
async def test(ctx):
    pagey = MyPaginator(title='Silly Paginator', colour=0xc67862, embed=True, timeout=90, use_defaults=True,
                        entries=[1, 2, 3], length=1, format='**')

    await pagey.start(ctx)
"""
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    load_data(bot)

# Read the dummy text in.
with open('dummy-text.txt') as fp:
    dummy_text = fp.read()

clarkson_gif = 'https://bit.ly/2JImWP2'

@pag.embed_generator(max_chars=2048)
def cooler_embed(paginator, page, page_index):
    embed = discord.Embed(colour=discord.Color.teal(), description=page)
    embed.set_image(url=clarkson_gif)
    return embed


@bot.command()
async def text(ctx):
    
    nav = pag.EmbedNavigatorFactory(factory=cooler_embed, max_lines=10)

    # Insert the dummy text into our factory.
    nav += dummy_text

    nav.start(ctx)

@bot.command(name='cribs', help='Link to Cam Cribs')
async def cribs(ctx):
    await ctx.send("Cam cribs: https://camcribs.com/")

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