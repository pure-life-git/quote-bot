import asyncio
import os
import random
import re
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents, case_insensitive=True)
bot.remove_command("help")
bot_color = discord.Color.from_rgb(21, 96, 189)

token = os.getenv("TOKEN")

conn = sqlite3.connect("bot.db")
cur = conn.cursor()


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    num_servers = len(bot.guilds)
    print(f"Monitoring {num_servers} servers!")

    # * TODO: Auto update based on bot.guilds vs SELECT *


@bot.command(name="ping", aliases=["p"])
async def ping(ctx):
    await ctx.send("Pong")


@bot.command(name="quote", aliases=["q"])
async def quote(ctx: commands.Context, channel: discord.TextChannel):
    messages = [message async for message in channel.history()]
    rdm = random.choice(messages)
    rdm_content = rdm.content
    raw_split = re.split('"(.*?)"', rdm_content)
    raw_poem = raw_split[1]
    raw_scribe = raw_split[2].split("-", maxsplit=2)[1]
    if raw_scribe[0] == " ":
        raw_scribe = raw_scribe[1:]
    raw_scribe = raw_scribe.split(" ")[0]
    await ctx.send(f'"{raw_poem}"')
    try:
        msg = await bot.wait_for(
            "message", check=lambda m: m.author == ctx.author, timeout=30.0
        )
        if msg.content.lower() == raw_scribe.lower():
            await ctx.send(f"Correct! You win.\nSee original message: {rdm.jump_url}")
            return
        else:
            await ctx.send(
                f"So close! The correct answer was {raw_scribe}.\nSee original message: {rdm.jump_url}"
            )
            return
    except asyncio.TimeoutError:
        await ctx.send(
            f"Challenge timed out! The correct answer was {raw_scribe}!\nSee original message: {rdm.jump_url}"
        )
        return


@bot.command(name="kill", aliases=["k"])
async def kill(ctx: commands.Context):
    file_name = "kill_switch"
    kill_state = os.path.isfile(file_name)
    print("Before:", kill_state)
    if kill_state:
        os.remove(file_name)
    else:
        f = open(file_name, "x")
        f.close()

    kill_msg = (
        ":rotating_light: Kill Mode: Activated :rotating_light:"
        if kill_state == False
        else ":x: Kill Mode: Deactivated :x:"
    )
    await ctx.send(kill_msg)


@bot.event
async def on_voice_state_update(
    member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
):
    death_note = [
        bot.get_user(221115052038684683)  # stafford
        # bot.get_user(288710564367171595)  #theo
    ]

    # if the member is stafford
    if os.path.isfile("kill_switch") and member in death_note:
        if not before.channel and after.channel:
            await member.move_to(None)
        return

    # if member.guild.get_role(1241950590725128272) in member.roles and (before.self_stream == False and after.self_stream == True):
    #     sleeper_agent = random.randint(30,300)
    #     print(f"Booting {member.name} in {sleeper_agent} seconds")

    #     theo = bot.get_user(288710564367171595)
    #     await theo.send(content=f"Booting {member.name} in {sleeper_agent} seconds")

    #     await asyncio.sleep(sleeper_agent)

    #     await member.move_to(member.guild.get_channel(1241961286774952007))
    #     await member.move_to(member.guild.get_channel(644075079558365188))

    #     await member.send(content="Certified Stafford moment", tts=True)


bot.run(token)
