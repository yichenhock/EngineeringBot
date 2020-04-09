from discord.ext import commands
from discord.ext import buttons


class MyPaginator(buttons.Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @buttons.button(emoji='\u23FA')
    async def record_button(self, ctx, member):
        await ctx.send('This button sends a silly message! But could be programmed to do much more.')

    @buttons.button(emoji='my_custom_emoji:1234567890')
    async def silly_button(self, ctx, member):
        await ctx.send('Beep boop...')

