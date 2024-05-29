import discord
from discord.ext import commands
import asyncio
import json as js
import random
import re

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '?', intents = intents, case_insensitive = True)
bot.remove_command('help')
bot_color = discord.Color.from_rgb(21, 96, 189)

token = "MTE1ODI2NzQxOTI5MTI4NzYxMg.GHoFGA.GMC5HHXW_tVLzog203fvJXRNH8SIMxDR3Fgwcs"
kill_var = False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="quote", aliases=["q"])
async def quote(ctx: commands.Context, channel: discord.TextChannel):
    messages = [message async for message in channel.history()]
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
    
# @bot.command(name="kill", aliases=["k"])
# async def kill(ctx: commands.Context):
#     f = open(ctx.guild.name + ".pkl", "rb")
#     d = pickle.load(f)
#     kill_var = d["kill_var"]
#     kill_var = not kill_var
#     d["kill_var"]
#     kill_msg = ":rotating_light: Kill Mode: Activated :rotating_light:" if kill_var == True else ":x: Kill Mode: Deactivated :x:"
#     await ctx.send(kill_msg)
    
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    staff = bot.get_user(221115052038684683)

    #if the member is stafford
    if kill_var and member == staff:
        if not before and after:
            await member.disconnect()
        return
    
    if member.guild.get_role(1241950590725128272) in member.roles and after.self_stream == True:
        await member.move_to(member.guild.get_channel(1241961286774952007))
        await member.move_to(member.guild.get_channel(644075079558365188))
        await member.send(content="Certified Stafford moment", tts=True)



bot.run(token)