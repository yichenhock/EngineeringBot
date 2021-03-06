import asyncio
import random
from math import ceil
from string import ascii_lowercase

import discord
from discord.ext import commands

import items
import lecturers
import tips
from constants import (DATA_PATH, LABS_OPTIONS, SC_EMOJI, SC_LAB, SC_LECTURE,
                       SC_LECTURE_INCREASE_PER_LEVEL, XP_INCREASE_PER_LEVEL,
                       XP_LAB, XP_LECTURE, XP_TO_LEVEL_UP, XP_TRIVIA_CORRECT,
                       XP_TRIVIA_INCORRECT)
from data import (add_data, get_data, get_labs_subset,
                  save_data)
from trivia_questions import get_trivia_questions

class StudyCommands(commands.Cog,name="Study"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='lab',help="Do a lab for {}**Standard Credit**.".format(SC_EMOJI))
    @commands.cooldown(1, 3600*3, commands.BucketType.user)
    async def lab(self,ctx): 

        labs_subset = get_labs_subset(LABS_OPTIONS)

        output = "Select a lab by typing what is in `this text`:"
        options = {}
        for lab in labs_subset:
            output += "\n\n- `{}` **{}** \n\t\t*{}*".format(lab["option"], lab["name"], lab["description"])
            options[lab["option"]] = lab

        def check(m):
            return m.author == ctx.author and (m.content in options)

        await ctx.send('',embed=discord.Embed(
                            description=output,
                            colour=discord.Color.greyple())
                            )

        msg = await self.bot.wait_for('message', check=check, timeout=120)
        lab = options[msg.content]
        outcome = random.choice(lab["outcomes"])
        output = "*{}*".format(outcome["description"])

        base_sc = SC_LAB
        multiplier = random.uniform(outcome["min_sc"], outcome["max_sc"])
        item_boost = items.get_player_boost(ctx.author.id, "labs")
        sc_add = round(base_sc * multiplier * (1+item_boost))
        player_sc = get_data(ctx.author.id, "sc", default_val=0)
        add_data(ctx.author.id, "sc", player_sc + sc_add)

        output += "\n\nYour demonstrator gave you {} **{}**.".format(SC_EMOJI, sc_add)
        if item_boost:
            output += "\n_**{:.1f}%** boost from_ **Labs** _items in your inventory._".format(item_boost*100)
        output += "\n\nYou get **`{}`<:xp:699934983074349086>**.".format(XP_LAB)
        lab_disp = discord.Embed(description=output,
                            colour = discord.Color.greyple())
        lab_disp.set_author(name=lab["name"],
                            url='',icon_url=ctx.author.avatar_url)
        await ctx.send('',embed=lab_disp)
        await give_xp(ctx, ctx.author.id, XP_LAB)

        await ctx.send(tips.get_random_tip())

        # stdc = get_data(ctx.author.id, "sc", default_val=0)
        # add_sc = random.randint(1,10)
        # add_data(ctx.author.id, "sc", stdc+add_sc)

        # string = "You did a lab for {}`{}`!".format(SC_EMOJI,add_sc)
        # tip = tips.get_random_tip(0.4)
        # if tip:
        #     string = tip + "\n\n" + string
        # await ctx.send(string)
        # await give_xp(ctx, ctx.author.id, XP_LAB)


    @commands.command(name='lecture',help="Go to a lecture for {}**Standard Credit**.".format(SC_EMOJI))
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def lecture(self,ctx):
        tip = tips.get_random_tip()
        if tip:
            await ctx.send(tip)

        player_level = get_data(ctx.author.id, "level", default_val=0)
        lec = lecturers.get_by_level(player_level)

        message = "Your current lecture series is **{}** by **{}**.".format(lec.subject, lec.name)

        base_sc = SC_LECTURE + SC_LECTURE_INCREASE_PER_LEVEL * player_level
        boost = items.get_player_boost(ctx.author.id, lec.category)

        sc = ceil(base_sc * (1+boost))
        player_sc = get_data(ctx.author.id, "sc", default_val=0)
        add_data(ctx.author.id, "sc", player_sc + sc)
        message += "\n\nYou went to the lecture and earned {} **{}**.".format(SC_EMOJI, sc)
        if boost > 0:
            message += "\n_**{:.1f}%** boost from_ **{}** _items in your inventory._".format(boost*100, lec.category.title())
        else:
            message += "\n\n> _Get items that boost **{}** in order to increase earnings._".format(lec.category.title())

        message += "\n\nYou get **`{}`<:xp:699934983074349086>**.".format(XP_LECTURE)

        file = discord.File(DATA_PATH+"lecturer_img/"+lec.image, filename=lec.image)
        lecture_disp=discord.Embed(description=message,colour=discord.Color.greyple())
        lecture_disp.set_thumbnail(url="attachment://"+lec.image)
        await ctx.send(file=file,embed=lecture_disp)

        if player_level == 2 and get_data(ctx.author.id, "inv", "Pills", default_val=0) > 0:
            # 'Tucker looks especially depressed today. After the lecture, you went to him and gave him an anti-depressant.'
            # '"What is this, bah humbug" said Tucker as he took the pill. But soon after it entered his mouth, something lit up in his eyes as he gazed longingly into the middle distance.'
            # '"Where has this been all my life", a tear rolled down Tucker's cheek as he turned to you. "Thank you, friend."'
            # '"I just had a revelation that I shouldn't be here, I'm gonna retire. You get a pass."'
            add_data(ctx.author.id, "xp", 0)
            add_data(ctx.author.id, "level", player_level + 1)
            pills = get_data(ctx.author.id, "inv", "Pills", default_val=0)
            add_data(ctx.author.id, "inv", "Pills", pills - 1)
            await show_level_up(ctx, player_level + 1)
            return
        await give_xp(ctx, ctx.author.id, XP_LECTURE)


    @commands.command(name='trivia', aliases = ["study", "question", "learn", "q","supo", "supervision"], help=
        """Answer a question to get standard credit.
        You get {}**Standard Credit** for correct answers and XP for both correct and incorrect answers.

        Aliases: `study`, `question`, `learn`, `q`, `supo`, `supervision`
        """.format(SC_EMOJI))
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def trivia(self,ctx):
        user_level = get_data(ctx.author.id, "level", default_val=0)

        # -- Picking question
        questions = get_trivia_questions()
        questions_todo = get_data(ctx.author.id, "questions_todo", default_val=[])

        if not questions_todo or max(questions_todo) >= len(questions):
            questions_todo = list(range(len(questions)))
            random.shuffle(questions_todo)
            add_data(ctx.author.id, "questions_todo", questions_todo)

        question_index = questions_todo[0]
        question = questions[question_index]


        # -- Getting answers
        if question.is_multiple_choice:
            answers = random.sample(question.answers, len(question.answers))
        else:
            answers = question.answers

        # -- Outputting question
        lec = lecturers.get_by_level(user_level)
        output = lecturers.get_by_level(user_level).get_trivia_message() + "\n\n"
        source = question.source
        if source:
            output += "> Source: *{}*\n{}\n".format(source, question.question_text)
        else:
            output += "{}\n".format(question.question_text)

        if question.is_multiple_choice:
            for i in range(len(answers)):
                output += "\n*{}) {}*".format(ascii_lowercase[i], answers[i])

            output += "\n\n**Type in the character of the answer you think is correct!**"
            def check(m):
                return m.author == ctx.author and (m.content in ascii_lowercase[:len(answers)]) and len(m.content) == 1
        else:
            output += "\n**Type in `answer` followed by what you think the answer is!**"
            def check(m):
                return m.author == ctx.author and len(m.content.split(maxsplit=1)) == 2 and (m.content.split(maxsplit=1)[0].lower() == "answer")

        thumbnail_file = discord.File(DATA_PATH+"lecturer_img/"+lec.image, filename=lec.image)
        trivia_disp=discord.Embed(description=output,
                        colour=discord.Color.greyple())
        trivia_disp.set_thumbnail(url="attachment://"+lec.image)
        trivia_disp.set_author(name="Supervision with {}".format(lec.name),
                            url='',icon_url=ctx.author.avatar_url)

        image_name = question.image
        if image_name:
            image_file =discord.File(DATA_PATH+"trivia_img/"+image_name, filename=image_name)
            trivia_disp.set_image(url="attachment://"+image_name)
            await ctx.send(files=(thumbnail_file, image_file), embed=trivia_disp)
        else:
            await ctx.send(file=thumbnail_file,embed=trivia_disp)

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=1800)
        except asyncio.TimeoutError:
            await ctx.send("{}, your trivia question timed out.".format(ctx.author.mention))
        else:
            if question.is_multiple_choice:
                letter = msg.content
                pos = ascii_lowercase.index(letter, 0, len(answers))
                answer = answers[pos]
            else:
                answer = msg.content.split(maxsplit=1)[1]

            # Remove question_index from questions_todo
            questions_todo.remove(question_index)

            # -- Acting depending on if answer is correct or not
            if question.is_correct(answer):
                xp = XP_TRIVIA_CORRECT
                # Get boosts and give
                base_sc = question.sc_reward
                category_boost = items.get_player_boost(ctx.author.id, question.category)
                supo_boost = items.get_player_boost(ctx.author.id, "supervisions")
                boost = category_boost + supo_boost
                sc_add = ceil(base_sc * (1+boost))
                player_sc = get_data(ctx.author.id, "sc", default_val=0)
                add_data(ctx.author.id, "sc", player_sc + sc_add)
                # Output message
                output = "{}, **Correct!**\n{}\nYou earned {} **{}**.".format(ctx.author.mention, question.answer_message, SC_EMOJI, sc_add)
                if boost > 0:
                    if category_boost and supo_boost:
                        boost_s = "{} and Supervisions".format(question.category.title())
                    elif category_boost:
                        boost_s = "{}".format(question.category.title())
                    elif supo_boost:
                        boost_s = "Supervisions"
                    output += "\n_**{:.1f}%** boost from_ **{}** _items in your inventory._".format(boost*100, boost_s)
            else:
                xp = XP_TRIVIA_INCORRECT
                if question.is_multiple_choice:
                    correct_letter = ascii_lowercase[answers.index(question.correct_answer)]
                    output = "{}, **Incorrect.**\n\nThe correct answer was **{}) {}**\n{}".format(ctx.author.mention, correct_letter, question.correct_answer, question.answer_message)
                else:
                    output = "{}, **Incorrect.**\n\nA correct answer was **{}**\n{}".format(ctx.author.mention, question.answers[0], question.answer_message)
                # Add the question back in so you do it again
                questions_todo.insert(4, question_index)

            add_data(ctx.author.id, "questions_todo", questions_todo)

            output += "\n\nYou get **`{}`<:xp:699934983074349086>**.".format(xp)

            file = discord.File(DATA_PATH+"lecturer_img/"+lec.image, filename=lec.image)
            trivia_disp=discord.Embed(description=output,
                            colour=discord.Color.greyple())
            trivia_disp.set_thumbnail(url="attachment://"+lec.image)
            trivia_disp.set_footer(text="Got an issue with this question, or want to add your own? \nMessage @Chen or go to https://forms.gle/dnxpaXPVUxEqoNpk9")
            await ctx.send(file=file,embed=trivia_disp)

            await give_xp(ctx, ctx.author.id, xp)

    @lab.error
    async def lab_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            hrs = int(error.retry_after // 3600)
            mins = int((error.retry_after % 3600) // 60)
            secs = ceil((error.retry_after%3600) % 60)
            desc = "Your lab hasn't begun yet! Your demonstrator will be here in `{}` hrs, `{}` mins, `{}` secs".format(hrs, mins, secs)
            msg = discord.Embed(description=desc,
                                colour=discord.Color.red())
            await ctx.send('',embed=msg)

    @lecture.error
    async def lecture_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            desc = "Your next lecture is in `{}` minutes, `{}` seconds".format(int(error.retry_after // 60), ceil(error.retry_after)%60)
            msg = discord.Embed(description=desc,
                                colour=discord.Color.red())
            await ctx.send('',embed=msg)

    @trivia.error
    async def trivia_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            desc = "Your next question is in `{}` minutes, `{}` seconds".format(int(error.retry_after // 60), ceil(error.retry_after)%60)
            msg = discord.Embed(description=desc,
                                colour=discord.Color.red())
            await ctx.send('',embed=msg)

    @commands.command(name='cribs', aliases=["crib"],help='Link to Cam Cribs')
    async def cribs(self,ctx):
        await ctx.send("Cam cribs: https://camcribs.com/")


async def give_xp(ctx, p_id, amount):
    level = int(get_data(p_id, "level", default_val=0))
    current_xp = int(get_data(p_id, "xp", default_val=0))
    new_xp = current_xp + amount
    xp_required = XP_TO_LEVEL_UP + XP_INCREASE_PER_LEVEL * level
    while new_xp >= xp_required:
        new_xp -= xp_required
        level += 1
        xp_required = XP_TO_LEVEL_UP + XP_INCREASE_PER_LEVEL * level
        await show_level_up(ctx, level)

    add_data(p_id, "level", level)
    add_data(p_id, "xp", new_xp)

async def show_level_up(ctx, level):
    message = ""
    lec = lecturers.get_by_level(level)
    message += ":tada: Your new lecturer is: **{}**! :tada:".format(lec.name)
    message += "\n\n_Get items that boost **{}** in order to increase lecture earnings._".format(lec.category.title())

    file = discord.File(DATA_PATH+"lecturer_img/"+lec.image, filename=lec.image)

    levelup_disp=discord.Embed(description=message,
                    colour=discord.Color.greyple())
    levelup_disp.set_author(name="Level Up to Level {}!".format(level),
                        url='',icon_url=ctx.author.avatar_url)
    levelup_disp.set_thumbnail(url="attachment://"+lec.image)
    await ctx.send(file=file,embed=levelup_disp)

def get_xp_string(player, amount):
    return "You get **`{}`<:xp:699934983074349086>**.".format(amount)

def setup(bot):
    bot.add_cog(StudyCommands(bot))
