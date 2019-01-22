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
