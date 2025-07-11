import asyncio
import datetime
import os
import random
import re
import sqlite3
import time

import discord
from discord.commands import options
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot(command_prefix="?", intents=discord.Intents.all())
bot_color = discord.Color.from_rgb(21, 96, 189)

token = os.getenv("TOKEN")

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

guild_ids = {"truck_stop": 644075079558365184, "alley": 599808865093287956}


@bot.event
async def on_ready():
    await bot.sync_commands()
    print(f"{bot.user.name} has connected to Discord!")
    num_servers = len(bot.guilds)
    print(f"Monitoring {num_servers} servers!")


# NOTE: Testing command to ensure bot's connection to discord
@bot.slash_command(name="ping", description="Test ping command")
async def ping(ctx):
    await ctx.respond("Pong!")


# NOTE: Main quote command. Gives a quote and allows the user to
# NOTE: guess who said it
@bot.slash_command(
    name="quote",
    description="Name the person who said the quote!",
    guild_ids=[guild_ids["alley"], guild_ids["truck_stop"]],
)
async def quote(ctx, channel: discord.TextChannel):
    await ctx.defer()

    messages = [message async for message in channel.history()]
    rdm = random.choice(messages)
    rdm_content = rdm.content

    raw_split = re.split('"(.*?)"', rdm_content)
    raw_poem = raw_split[1]
    raw_scribe = raw_split[2].split("-", maxsplit=2)[1]

    if raw_scribe[0] == " ":
        raw_scribe = raw_scribe[1:]
    raw_scribe = raw_scribe.split(" ")[0]

    await ctx.respond(f'"{raw_poem}"')

    try:
        msg = await bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=30.0
        )
        if msg.content.lower() == raw_scribe.lower():
            await ctx.followup.send(
                f"Correct! You win.\nSee original message: {rdm.jump_url}"
            )
            return
        else:
            await ctx.followup.send(
                f"So close! The correct answer was {raw_scribe}.\nSee original message: {rdm.jump_url}"
            )
            return
    except asyncio.TimeoutError:
        await ctx.followup.send(
            f"Challenge timed out! The correct answer was {raw_scribe}!\nSee original message: {rdm.jump_url}"
        )
        return


def get_timer_progress(duration, start_time):
    cur_time = time.time()
    finish_time_ts = start_time + duration
    time_left_secs = finish_time_ts - cur_time

    time_left_percent = 100 - (round((time_left_secs / duration) * 100))

    time_left = datetime.timedelta(seconds=time_left_secs)

    finish_time = datetime.datetime.fromtimestamp(finish_time_ts)
    finish_time_form = finish_time.strftime("%H:%M:%S")

    return {
        "percent": time_left_percent,
        "time_left": time_left,
        "finish_time": finish_time,
        "finish_time_ts": finish_time_ts,
        "finish_time_form": finish_time_form,
    }


@bot.slash_command(name="timer")
async def set_timer(ctx, hours: int = 0, minutes: int = 0, seconds: int = 0):
    start_time = time.time()
    timer_time = (hours * 3600) + (minutes * 60) + seconds
    finish_time = start_time + timer_time
    pretty_time = (
        (str(hours) + "h")
        if hours > 0
        else (
            "" + (str(minutes) + "m")
            if (minutes > 0 or hours > 0)
            else "" + (str(seconds) + "s")
        )
    )
    res = get_timer_progress(timer_time, start_time)
    message = await ctx.respond(f"Timer set for {hours}h {minutes}m {seconds}s")
    while time.time() < finish_time:
        res = get_timer_progress(timer_time, start_time)
        timer_embed = discord.Embed(
            title=pretty_time + " Timer",
            color=bot_color,
            timestamp=res["finish_time"],
        )
        timer_embed.set_footer(text="Timer finishes at")
        progress_string = ""
        for i in range(0, 10):
            if (i * 10) > res["percent"]:
                progress_string += ":new_moon:"
            else:
                progress_string += ":full_moon:"

        timer_embed.add_field(name="Percent", value=res["percent"])
        timer_embed.add_field(name="Time Left", value=res["time_left"])
        timer_embed.add_field(name="Finish Time", value=res["finish_time_form"])
        timer_embed.add_field(name="Completion", value=progress_string)

        await message.edit_original_response(content="", embeds=[timer_embed])
        await asyncio.sleep(0.5)

    timer_embed = discord.Embed(
        title=pretty_time + " Timer",
        description=f"Timer finished!",
        color=bot_color,
        timestamp=res["finish_time"],
    )
    timer_embed.set_footer(text="Timer finished at")
    timer_embed.add_field(name="Percent", value="100%")
    timer_embed.add_field(name="Time Left", value="00:00:00")
    timer_embed.add_field(name="Finish Time", value=res["finish_time_form"])
    timer_embed.add_field(
        name="Completion",
        value=":full_moon::full_moon::full_moon::full_moon::full_moon::full_moon::full_moon::full_moon::full_moon::full_moon:",
    )

    await message.edit_original_response(embeds=[timer_embed])


# @bot.slash_command(name="rps")
# @options("choice")
# def rps(ctx: discord.ApplicationContext, choice: str)


@bot.event
async def on_message(msg: discord.Message):
    print("got a message")
    print(msg)
    daniel = bot.get_user(149337676343017472)
    theo = bot.get_user(288710564367171595)


#    if (
#        msg.author in [daniel, theo]
#        and msg.channel == bot.get_channel(644075079558365187)
#        and len(msg.attachments) != 0
#        and msg.attachments[0].content_type.startswith("image")
#    ):
#        await msg.reply(content="Haha this is so funny am i right guys?")


bot.run(token)
