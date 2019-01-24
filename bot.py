import discord
from discord import Game
from discord.ext import commands
import asyncio
import time
import json
import os
import random
import requests
from itertools import cycle
from discord import Game
from discord.voice_client import VoiceClient
from discord import Member
from discord.ext.commands import has_permissions


startup_extensions = ['Music','serverinfo','autorole','fun','Mod','ModLog','welcomr','embed','translate','polls','level']
Bot = discord.Client
bot = commands.Bot('boi ')
botdiscord = discord.Client()

@bot.event
async def on_ready():
    print('▁ ▂ ▄ ▅ ▆ ▇ █ ----- █ ▇ ▆ ▅ ▄ ▂ ▁')
    print('▁         Bot Online As')
    print("▁         Name: {}  ".format(bot.user.name))
    print("▁         ID: {}  ".format(bot.user.id))
    servers = list(bot.servers)
    print("▌│█║▌║▌║ Connected to " + str(len(bot.servers))+" servers: ")
   # for x in range(len(servers)):
       # print('▌│█║▌║▌║ '+ servers[x-1].name + ' / ' + servers[x-1].id+' ')
    print('▁ ▂ ▄ ▅ ▆ ▇ █ ----- █ ▇ ▆ ▅ ▄ ▂ ▁')

@bot.event
async def on_message(message):
    t = open("storage/users.json", "r")
    users = json.load(t)

    if message.author.bot:
        return
    if message.channel.is_private:
        return
    else:
        await update_data(users, message.author)
        number = random.randint(5,10)
        await add_experience(users, message.author, number)
        await level_up(users, message.author, message.channel)

    with open("storage/users.json", "w") as f:
        json.dump(users, f)
    await bot.process_commands(message)


async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]["xp"] = 0
        users[user.id]["level"] = 1
        users[user.id]["last_message"] = 0

async def add_experience(users, user, exp):
    if time.time() - users[user.id]["last_message"] > 30:
        users[user.id]["xp"] += exp
        users[user.id]["last_message"] = time.time()
        print("player {}/{} gained {} xp".format(user.name, user.id, exp))
    else:
         return

async def level_up(users, user, channel):
    experience = users[user.id]["xp"]
    lvl_start = users[user.id]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await bot.send_message(channel, ":tada: Congrats {}, you levelled up to level {}!".format(user.mention, lvl_end))
        users[user.id]["level"] = lvl_end
        print("player {}/{} leveled up with {} xp".format(user.name, user.id, experience))

@bot.command(pass_context=True)
async def leaderboard(ctx):
    t = open("storage/users.json", "r")
    users = json.load(t)
    experience = users[ctx.message.author.id]["xp"]
    lvl_start = users[ctx.message.author.id]["level"]
    high_score_list = sorted(users, key=lambda x : users[x].get('xp', 0), reverse=True)
    embed=discord.Embed(title='Leaderboard', description='Leaderboard for {}'.format(ctx.message.server.name), color=0xff00f6)
    for number, user in enumerate(high_score_list):
        embed.add_field(name='{}.'.format(number + 1), value='{0} with {1}xp\n'.format(ctx.message.author.server.get_member(user), users[user].get('xp', 0)), inline=False)
    await bot.send_message(ctx.message.channel, embed=embed)
    
@bot.command(pass_context=True)
async def about(ctx):
    servers = bot.servers
    members = bot.get_all_members()
    messages = bot.messages
    channels = bot.get_all_channels()
    embed=discord.Embed(title='Bot information', description='[Support Server Invite](https://discord.gg/hGaayXq)', color=0xff00f6)
    em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name='Servers', value=f'Currently in {str(len(servers))} servers.')
    embed.add_field(name='Online Users', value=str(len({m.id for m in bot.get_all_members() if m.status is not discord.Status.offline})))
    embed.add_field(name='Total Users', value=str(len({m.id for m in bot.get_all_members()})))
    embed.add_field(name='Channels', value=f"{sum(1 for g in bot.servers for _ in g.channels)}")
    embed.add_field(name="Library", value=f"discord.py")
    embed.add_field(name="Invite", value=f"[Click Here](https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=268905542)")
    embed.add_field(name="Upvote this bot!", value=f"[Click here](https://discordbots.org/bot/{bot.user.id}) :reminder_ribbon:")
    embed.set_footer(text="BaguetteBot | By AlexOp")
    await bot.say(embed=embed)

@commands.command(aliases=['trump', 'trumpquote'])
    async def asktrump(self, ctx, *, question):
        '''Ask Donald Trump a question!'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}') as resp:
                file = await resp.json()
        quote = file['message']
        em = discord.Embed(color=discord.Color.green())
        em.title = "What does Trump mean?"
        em.description = quote
        em.set_footer(text="Trump", icon_url="http://www.stickpng.com/assets/images/5841c17aa6515b1e0ad75aa1.png")
        await ctx.send(embed=em)
        
class Main_Commands():
    def __init__(self, bot):
        self.bot = bot

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run(str(os.environ.get('BOT_TOKEN'))))
