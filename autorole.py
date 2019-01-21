import discord
from discord.ext import commands
from discord.utils import get
from cogs.utils.dataIO.dataIO import js as dataIO
import os
import json

class Autorole:
    """Automatically assign roles to new members on join."""

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        role = get(member.server.roles, name="buddies")
        await self.bot.add_roles(member, role)
        await self.bot.send_message(self.bot.get_channel('444139338486382593'), 'Hello {} and welcome to Baguette Connect! We hope you have a good time here.'.format(member.mention))
        print("Added {} to new member with name: {}".format(role, member))

    async def on_member_remove(self, member):
        await self.bot.send_message(self.bot.get_channel('444139338486382593'), 'User {} Just left the server :disappointed_relieved: we are sorry to see you go.'.format(member.mention))
        print("Member with name: {}, just left".format(member))


def setup(bot):
    bot.add_cog(Autorole(bot))
    print("Loaded Autorole")
