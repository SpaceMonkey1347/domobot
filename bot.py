import os
import random
from dotenv import load_dotenv
import re

import logging

import discord
from discord.ext import commands

import messages as mes
from finance import lookup, usd
from cipher import nykro_cipher

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
assert isinstance(TOKEN, str)

intents = discord.Intents.all()
client = discord.Client(intents=intents)
help_command = commands.DefaultHelpCommand(show_parameter_descriptions=False)

prefix = '!!'
bot = commands.Bot(
        command_prefix=prefix,
        intents=intents,
        help_command=help_command
        )


handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w+')
message_logger = logging.FileHandler(filename='logs/mess.log', encoding='utf-8', mode='w+')
logging.basicConfig(filename='logs/mess.log', encoding='utf-8', level=logging.DEBUG)

# BOT EVENTS

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (id: {bot.user.id if bot.user else None})')


@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = guild.system_channel
    content = mes.welcome(member.mention)
    embed = discord.Embed(description=content)
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    await bot.process_commands(message)
    logging.info(message)


# BOT COMMANDS

@bot.command(
        brief="Send bot invite link",
        description="Send link to invite the bot to your server",
        )
async def invite(ctx):
    content = ('https://discord.com/oauth2/authorize?client_id=126288700519743'
               '9067&permissions=8&integration_type=0&scope=bot')
    emb = discord.Embed(title="Invite Link", description=content)
    await ctx.send(embed=emb)


@bot.command(
        brief="Ping the bot",
        description="Get the ping (in miliseconds) of the bot",
        )
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(
        brief='Quotes a random message from user in this channel',
        description=(
                'Quotes a random message from user in this channel\n'
                'Will only search past 200 messages\n'
                '### Usage:\n'
                f'`{bot.command_prefix}quote @name`\n'
                f'`{bot.command_prefix}quote name`\n`'
                f'`{bot.command_prefix}quote nickname`\n'
                f'`{bot.command_prefix}quote globalname`'
                ),
        )
async def quote(ctx, *args):
    input_string = " ".join(args).strip()
    if not input_string:
        title = "Quote"
        description = (
                '### Usage:\n'
                f'`{bot.command_prefix}quote [@name/name/nick/global]`'
                )
        message_embed = discord.Embed(title=title, description=description)
        await ctx.send(embed=message_embed)
        return

    user = None
    if args[0].startswith('<@') and args[0].endswith('>'):
        user_id = int(args[0][2:-1])
        user = ctx.guild.get_member(user_id)
    else:
        get = discord.utils.get
        user = (
            get(ctx.guild.members, name=input_string)
            or get(ctx.guild.members, global_name=input_string)
            or get(ctx.guild.members, nick=input_string)
            )

    if user is None:
        await ctx.send("User not found")
        return

    user_messages = [
            message async for message in ctx.channel.history(limit=200)
            if message.author == user and
            not message.content.startswith(bot.command_prefix)
            ]
    if not user_messages:
        await ctx.send(f"No recent messages found from {user}")
        return

    message = random.choice(user_messages)
    content = message.content
    attachments = message.attachments
    message_embed = discord.Embed(description=content)
    message_embed.set_author(name=str(user), icon_url=user.avatar.url)
    embeds = [message_embed]
    for att in attachments:
        image_emb = discord.Embed().set_image(url=att.url)
        embeds.append(image_emb)

    await message.reply(embeds=embeds, mention_author=False)


@bot.command(
        name='lookup',
        brief='Lookup stock price info by ticker symbol',
        description=(
            'Lookup stock\'s last closing price, price change,'
            ' and percent change by ticker symbol\n.'
            'Powered by Yahoo Finance (no association)'
            f'Usage: `{bot.command_prefix}lookup [ticker-symbol]`'
            'Example tickers: https://finance.yahoo.com/lookup/'
            ),
        )
async def lookup_stock(ctx, *args):
    arguments = ' '.join(args)
    if not args:
        title = 'lookup'
        usage = f'Usage: `{bot.command_prefix}lookup [ticker-symbol]`'
        embed = discord.Embed(title=title, description=usage)
        await ctx.send(embed=embed)
        return

    info = lookup(arguments)
    if not info:
        title = 'Invalid stock ticker symbol'
        examples = (
                '### Examples:\n'
                f'`{bot.command_prefix}lookup COST`\n'
                f'`{bot.command_prefix}lookup GOOG`\n'
                f'`{bot.command_prefix}lookup AAPL`'
                )
        embed = discord.Embed(title=title, description=examples)
        await ctx.send(embed=embed)
        return

    title = f'{str(args[0]).upper()}'
    stock_info = (
            f'Current Close: {usd(info[0])}\n'
            f'Price Change: {usd(info[1])}\n'
            f'Percent Change: {info[2]:,.2}%\n'
            f'https://finance.yahoo.com/quote/{args[0].upper()}'
            )
    embed = discord.Embed(title=title, description=stock_info)

    await ctx.send(embed=embed)


@bot.command(
        brief='Play the Monty Hall Problem',
        description=(
            'Play the Monty Hall Problem\n'
            'optional number of doors\n'
            '`doors` must be a number between 3 and 9 inclusive\n'
            f'Usage: `{prefix}monty [3-9]`'
            ),
        )
async def monty(ctx, *args):
    doors = '3'
    if args:
        doors = str(args[0])

    if not doors.isnumeric():
        content = 'Optional argument must be a number'
        await ctx.send(content)
        return

    doors = int(doors)
    if not 3 <= doors <= 9:
        content = 'Optional argument must be a between 3 and 9'
        await ctx.send(content)
        return

    content = (
            'Let\'s Make A Deal!\n'
            f'Behind one of {doors} doors is a brand new car, but behind the'
            ' other two is a goat. Click on a reaction to submit your choice!'
            )
    message = await ctx.send(content)
    for door in range(1, doors + 1):
        await message.add_reaction(mes.emojies[str(door)])

    def check(reaction, user):
        return user == ctx.author and str(reaction) in mes.emoji_to_numbers

    reaction = await bot.wait_for('reaction_add', timeout=600, check=check)

    car_door = random.randint(1, doors)
    user_choice = int(mes.emoji_to_numbers[str(reaction[0])])

    choices = [user_choice]
    alternative = car_door
    if user_choice == car_door:
        goats = [num for num in range(1, doors + 1)]
        goats.pop(car_door - 1)
        alternative = random.choice(goats)
    choices.append(alternative)
    revealed_doors = ", ".join([
        str(door) for door in range(1, doors + 1) if door not in choices
        ])

    content = (
            'I\'ll let you know that behind door '
            f' {revealed_doors} is a goat.\n'
            f'Do you want to stay on {user_choice}'
            f' or switch to door {alternative}?'
            )
    message = await ctx.send(content)
    for door in choices:
        await message.add_reaction(mes.emojies[str(door)])

    reaction = await bot.wait_for('reaction_add', timeout=600, check=check)

    if int(mes.emoji_to_numbers[str(reaction[0])]) == car_door:
        content = "Congrats! Enjoy your ride!\n# 🚗"
    else:
        content = "Congrats! You win a goat!\n# 🐐"
    await ctx.send(content)


@bot.command(
        brief='Roll dice in D&D format (ex: 3d6+10)',
        description=f"""
        Usage: `{prefix}role [#d#[+m]]... [flag]...`
        Default value: 1d20+0

        Roll # of dice with # of sides with optional [m] modifier
        # of dice can be negative (subtracting roll from modifier[s])
        Each roll (seperated by <Space>) is a calculated seperatly
        Dice can have any number of sides and be in any quantity
        Modifiers are numbers not next to a 'd'
        Modifiers not in roll arguments are added to sum total
        Rolls can have only one roll but any number of modifiers
        If number of dice is ommited, defaults to 1
        If number of sides is ommited, defaults to 20

        Flags: all flags can be added in any order

        Modifier Flags: you can use first 3 letter as a shorthand
        `[adv]antage`: roll with advantage
        `[dis]advantage`: roll with disadvantage
        `[emp]thasis`: roll with empthasis (take least average roll)

        Sum Flags: rules for how outputs are added together
        `sum-all`: sum total and indivisual rolls (default)
        `sum-total`: sum total of all rolls
        `sum-rolls`: sum indivisual rolls
        `sum-[pre]vious`: sum total with previous roll in channel
        `sum-none`: do not sum

        Scoped Flags: only one can be used per command
        `global`: apply flags for everyone in server (access: Mod)
        `party`: apply flags for everyone in party (access: DM)
        `@user`: apply flags for mentioned user (access: DM/Mod)

        Meta Flags: flags on how to process flags'
        `once-flags`: do flags for next roll only
        `keep-flags`: toggle flags or apply following flags
        `reset-flags`: resets personal (default) or scoped flags

        Examples:
        `{prefix}roll 2d6
        `{prefix}roll 6d`
        `{prefix}roll d100+10`
        `{prefix}roll sum-alike 15+2d2 3d2 4d6`
        `{prefix}roll sum-rolls 5d8-10 d20 -4d`
        `{prefix}roll adv 2d8+10`
        `{prefix}roll once-flags sum-rolls advantage @example`
        """,
        )
async def roll(ctx, *args):
    print("\nTEST\n")

    grand_total_mods = []
    grand_total = 0
    roll_totals = []
    rolls = []

    embed = discord.Embed(title='Rolls')

    # checks for correct argument syntax
    total_modifier_ptn = re.compile(r'^([+-]?[0-9]*)*$')
    roll_ptn = re.compile(
            # preceeding modifiers
            r'^([+-]?[0-9]+(?!d)[+-])*'
            # roll, ensure no double operator with r'(?<![+-])'
            r'((?<![+-])[+-])?[0-9]*d[0-9]*'
            # trailing modifiers
            r'([+-][0-9]+)*$'
            )

    # for retrieving lists of values from roll expression
    lead_mods_ptn = re.compile(r'^([+-]?[0-9]+(?![0-9]*d))+')
    trail_mods_ptn = re.compile(r'([+-][0-9]+)+$')

    # for directly retrieving values
    total_mods_ptn = re.compile(r'[+-]?[0-9]*')
    lead_mod_ptn = re.compile(r'[+-]?[0-9]+')
    trail_mod_ptn = re.compile(r'[+-][0-9]+')
    count_ptn = re.compile(r'[+-]*[0-9]+(?=d)')
    sides_ptn = re.compile(r'(?<=d)[0-9]+')

    if not args:
        args = ['1d20']

    for arg in args:
        if total_modifier_ptn.search(arg):
            modifiers = total_mods_ptn.findall(arg)
            for mod in modifiers:
                if not mod:
                    continue
                grand_total_mods.append(int(mod))
                grand_total += int(mod)

            print("TOTAL", arg)
            print("totals", modifiers)
            print("grand total", grand_total)
            print('')

        if roll_ptn.search(arg):
            # defaults
            modifier = 0
            count = 1
            sides = 20
            roll_values = []
            roll_total = 0

            # apply expressions
            lead_mods_match = lead_mods_ptn.search(arg)
            trail_mods_match = trail_mods_ptn.search(arg)
            count_match = count_ptn.search(arg)
            sides_match = sides_ptn.search(arg)

            # extract from regexes

            if lead_mods_match:
                modifiers = lead_mod_ptn.findall(lead_mods_match.group())
                for mod in modifiers:
                    modifier += int(mod)

            if trail_mods_match:
                modifiers = trail_mod_ptn.findall(trail_mods_match.group())
                for mod in modifiers:
                    modifier += int(mod)

            if count_match:
                count = int(count_match.group())

            if sides_match:
                sides = int(sides_match.group())

            # roll the dice
            for _ in range(abs(count)):
                value = random.randint(1, sides)
                value = value * -1 if count < 0 else value
                roll_values.append(value)
                roll_total += value

            # add it up
            roll_total += int(modifier)
            grand_total += roll_total

            embed.add_field(name=arg, value=(f'{modifier} + {roll_values}\n'
                                             f'={roll_total}'))

            # print("ROLL", arg)
            # print('modifier', modifier)
            # print('count', count)
            # print('sides', sides)
            # print('roll values', roll_values)
            # print('roll total', roll_total)
            # print('grand total', grand_total)
            # print('')

    embed.add_field(name='Grand Total', value=f'{grand_total}', inline=False)
    await ctx.send(embed=embed)


async def cipher(ctx):
    content = ctx.message.content
    reference = ctx.message.reference
    if reference:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        content = message.content
    content = content.replace(f"{bot.command_prefix}nykro_encipher ", "", 1)
    content = content.replace(f"{bot.command_prefix}nykro_decipher ", "", 1)
    return content


@bot.command(
        brief="Encipher your message using nykrocipher",
        description=f"""
        Encipher your message using nykrocipher.
        Usage: `{bot.command_prefix}nykro_encipher message`
        or reply to any message with `{bot.command_prefix}nykro_encipher`
        """,)
async def nykro_encipher(ctx):
    content = await cipher(ctx)
    await ctx.send(nykro_cipher(content, True))



@bot.command(
        brief="Decipher a Nykrociphered message",
        description=f"""
        Decipher a Nykrociphered message.
        Usage: `{bot.command_prefix}nykro_decipher message`
        or reply to any message with `{bot.command_prefix}nykro_decipher`
        """
        )
async def nykro_decipher(ctx):
    content = await cipher(ctx)
    await ctx.send(nykro_cipher(content, False))


@bot.command()
async def nword(ctx):
    pass


@bot.command()
async def top(ctx):
    pass


# @bot.command(
#         brief='',
#         description='',
#         )
# async def role(ctx, *args):
#     ...
#
#
# @bot.command(
#         name='reaction-role',
#         brief='',
#         description='',
#         )
# async def reaction_role(ctx, *args):
#     ...


bot.run(TOKEN, log_handler=handler)
