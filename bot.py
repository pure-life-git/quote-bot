import discord
from discord.ext import commands

import asyncio
import random
import re


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '?', intents = intents, case_insensitive = True)
bot.remove_command('help')
bot_color = discord.Color.from_rgb(21, 96, 189)

token = "MTE1ODI2NzQxOTI5MTI4NzYxMg.GHoFGA.GMC5HHXW_tVLzog203fvJXRNH8SIMxDR3Fgwcs"

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# @bot.event
# async def on_guild_join(guild: discord.Guild):
#     d = {"guild_id": guild.id}
#     f = open("bot.json", "a")
#     f.write(json.dumps(d, indent=4))
#     f.close()

@bot.command(name="quote", aliases=["q"])
async def quote(ctx, channel: discord.TextChannel):
    messages = [message async for message in  channel.history()]
    rdm = random.choice(messages)
    rdm_content = rdm.content
    raw_split = re.split('"(.*?)"', rdm_content)
    raw_poem = raw_split[1]
    raw_scribe = raw_split[2].split('-', maxsplit=2)[1]
    if raw_scribe[0] == " ":
        raw_scribe = raw_scribe[1:]
    raw_scribe = raw_scribe.split(" ")[0]
    await ctx.send(f'"{raw_poem}"')
    try:
        msg = await bot.wait_for('message', check = lambda m: m.author == ctx.author, timeout=30.0)
        if msg.content.lower() == raw_scribe.lower():
            await ctx.send(f"Correct! You win.\nSee original message: {rdm.jump_url}")
            return
        else:
            await ctx.send(f"So close! The correct answer was {raw_scribe}.\nSee original message: {rdm.jump_url}")
            return
    except asyncio.TimeoutError:
        await ctx.send(f"Challenge timed out! The correct answer was {raw_scribe}!\nSee original message: {rdm.jump_url}")
        return


bot.run(token)