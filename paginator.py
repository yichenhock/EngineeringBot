"""Embed paginator for paginating too large embes"""

import asyncio


# emojis for input
FAST_PREVIOUS = "\u23EA"  # [:track_previous:]
PREVIOUS = "\u25C0"  # [:arrow_left:]
NEXT = "\u25B6"  # [:arrow_right:]
FAST_NEXT = "\u23E9"  # [:track_next:]
DELETE_EMOJI = "\U0001F1FD"  # [:x:]

# unite the emojis in one list
#EMOJIS = [FAST_PREVIOUS, PREVIOUS, NEXT, FAST_NEXT, DELETE_EMOJI]
EMOJIS = [PREVIOUS, NEXT]

class Paginator:
    """
    Represents the interactive paginator.
    """
    def __init__(self, bot, ctx, pages, page_items, shop_commands, timeout):
        self.bot = bot
        self.ctx = ctx
        self.pages = pages
        self.page_items = page_items
        self.timeout = timeout
        self.shop_commands = shop_commands

        self.index = int()
        self.paginating = True

        self.emoji_selected = None
        self.emoji_func = {
            PREVIOUS: self.prev,
            NEXT: self.next,
        }

        self.custom_emojis = []


    async def add_page_emojis(self, page_num): # not using currently
        for item in self.page_items[page_num]:
            self.custom_emojis.append(str(item.emoji))
            asyncio.create_task(self.message.add_reaction(item.emoji))

    async def remove_page_emojis(self, page_num): # not using currently
        for item in self.page_items[page_num]:
            self.custom_emojis.remove(str(item.emoji))
            asyncio.create_task(self.message.remove_reaction(item.emoji, self.bot.user))
    
    async def handle_reaction(self):
        if self.emoji_selected in self.emoji_func:
            await self.emoji_func[self.emoji_selected]()
        else:
            await self.message.remove_reaction(self.emoji_selected, self.ctx.author)
            for page in self.page_items:
                i = None
                for item in page:
                    if str(item.emoji) == self.emoji_selected:
                        i = item
                if i:
                    await self.shop_commands.on_item_reacted(self.ctx, i)
            
            self.emoji_selected = None

    async def next(self):
        """Move to the next page."""
        if self.index != len(self.pages) - 1:
            self.index += 1
            #await self.remove_page_emojis(self.index - 1)
            #self.add_page_emojis(self.index)
        await self.message.remove_reaction(NEXT, self.ctx.author)

    async def prev(self):
        """Move to the previous page."""
        if self.index != 0:
            self.index -= 1
            #await self.remove_page_emojis(self.index + 1)
            #self.add_page_emojis(self.index)
        await self.message.remove_reaction(PREVIOUS, self.ctx.author)

    async def delete(self):
        """Delete the emojis. Session is terminated."""
        self.paginating = False
        await self.message.clear_reactions()

    def check(self, reaction, user):
        """Checks:
			If the emoji which is added is one of the emojis
			which are used as an input utility
			
			If the user who is adding emojis is the user
			who invoked the command
			
			If the messages are the same one."""
        if str(reaction.emoji) in EMOJIS + self.custom_emojis:
            self.emoji_selected = str(reaction.emoji)
        return (
            user == self.ctx.message.author
            and self.message.id == reaction.message.id
            and str(reaction.emoji) in EMOJIS + self.custom_emojis
        )

    async def run(self):
        """Main interactive loop for the paginator."""
        self.pages[self.index].set_footer(
            text=f"Page {self.index + 1}/{len(self.pages)}\nClick the arrows below to change page, and click emojis to buy items."
        )
        self.message = await self.ctx.send(embed=self.pages[self.index])

        for page in self.page_items:
            for item in page:
                self.custom_emojis.append(str(item.emoji))

        for emoji in EMOJIS + self.custom_emojis:
            self.bot.loop.create_task(self.message.add_reaction(emoji))
            #asyncio.create_task(self.message.add_reaction(emoji))
        
        #self.add_page_emojis(self.index)

        while self.paginating:
            try:
                await self.wait_first(
                    self.wait_for_reaction_add(), self.wait_for_reaction_remove()
                )
            except asyncio.TimeoutError:
                self.paginating = False
                await self.message.clear_reactions()
                self.pages[self.index].set_footer(text=f"Paginator timed out")
                await self.message.edit(embed=self.pages[self.index])
            else:
                await self.handle_reaction()
                if self.paginating:
                    self.pages[self.index].set_footer(
                        text=f"Page {self.index + 1}/{len(self.pages)}\nClick the arrows below to change page, and click emojis to buy items."
                    )
                    await self.message.edit(embed=self.pages[self.index])
                else:
                    self.pages[self.index].set_footer(text=f"Paginator closed")
                    await self.message.edit(embed=self.pages[self.index])

    async def wait_first(self, *futures):
        """Wait for reaction add or reaction remove."""
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        gather = asyncio.gather(*pending)
        gather.cancel()
        try:
            await gather
        except asyncio.CancelledError:
            pass
        return done.pop().result()

    async def wait_for_reaction_add(self):
        """Wait for reaction add."""
        return await self.bot.wait_for(
            "reaction_add", check=self.check, timeout=self.timeout
        )

    async def wait_for_reaction_remove(self):
        """Wait for reaction remove."""
        return await self.bot.wait_for(
            "reaction_remove", check=self.check, timeout=self.timeout
        )