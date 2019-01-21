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
    g = open("storage/Servers.json", "r")
    servers = json.load(g)
    t = open("storage/users.json", "r")
    users = json.load(t)

    if message.author.bot:
        return
    if message.channel.is_private:
        return
    else:
        await update_data(users, message.author, message.server, servers)
        number = random.randint(5,10)
        await add_experience(users, message.author, number, message.server, servers)
        await level_up(users, message.author, message.channel, message.server, servers)

    with open("storage/users.json", "w") as f:
        json.dump(users, f)
    with open("storage/Servers.json", "w") as k:
        json.dump(servers, k)
    await bot.process_commands(message)


async def update_data(users, user, server, servers):
    if not user.id + "-" + server.id in users:
        users[user.id + "-" + server.id] = {}
        users[user.id + "-" + server.id]["experience"] = 0
        users[user.id + "-" + server.id]["level"] = 1
        users[user.id + "-" + server.id]["last_message"] = 0
    if not server.id in servers:
        servers[server.id] = {}
        servers[server.id]["disabled"] = "false"

async def add_experience(users, user, exp, server, servers):
    if time.time() - users[user.id + "-" + server.id]["last_message"] > 30:
        users[user.id + "-" + server.id]["experience"] += exp
        users[user.id + "-" + server.id]["last_message"] = time.time()
        print("player {}/{} gained {} xp".format(user.name, user.id, exp))
    else:
         return

async def level_up(users, user, channel, server, servers):
    experience = users[user.id + "-" + server.id]["experience"]
    lvl_start = users[user.id + "-" + server.id]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await bot.send_message(channel, ":tada: Congrats {}, you levelled up to level {}!".format(user.mention, lvl_end))
        users[user.id + "-" + server.id]["level"] = lvl_end
        print("player {}/{} leveled up with {} xp".format(user.name, user.id, experience))

@bot.command(pass_context=True)
async def leaderboard(ctx):
    t = open("storage/users.json", "r")
    users = json.load(t)
    experience = users[ctx.message.author.id + "-" + ctx.message.server.id]["experience"]
    lvl_start = users[ctx.message.author.id + "-" + ctx.message.server.id]["level"]
    high_score_list = sorted(users, key=lambda x : users[x].get('lvl_start', 0), reverse=True)
    message = ''
    for number, user in enumerate(high_score_list):
        message += '{0}. {1} with {2}xp\n'.format(number + 1, ctx.message.author, ctx.message.author.id + "-" + server.id.get('lvl_start', 0))
    await bot.send_message(ctx.message.channel, message)

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
