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

class levels:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(levels(bot))
