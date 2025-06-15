import asyncio
import os
import random
import re
import sqlite3
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

# from siegeapi import Auth

load_dotenv()


bot = discord.Bot(command_prefix="?", intents=discord.Intents.all())
bot_color = discord.Color.from_rgb(21, 96, 189)


token = os.getenv("TOKEN")

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

# siege_auth = Auth(os.getenv("UBI_EMAIL"), os.getenv("UBI_PSWD"))

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


@bot.slash_command(
    name="timer",
    guild_ids=[
        "599808865093287956",
    ],
)
async def set_timer(ctx, hours: int = 0, minutes: int = 0, seconds: int = 0):

    timer_embed = discord.Embed(
        title="Timer",
        description=f"Timer set for {hours}h {minutes}m {seconds}s",
        color=bot_color,
    )

    timer_embed.add_field(name="Test Field", value=":rotating_light:")

    await ctx.respond(
        f"Timer set for {hours}h {minutes}m {seconds}s", embeds=[timer_embed]
    )
    timer_time = (hours * 3600) + (minutes * 60) + seconds

    await asyncio.sleep(timer_time)

    await ctx.followup.send(":rotating_light: Timer done! :rotating_light:")


bot.run(token)
