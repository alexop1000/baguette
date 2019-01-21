import discord
from discord.ext import commands
import time
import json                                                            #▁ ▂ ▄ ▅ ▆ ▇ █ ADMIN COMMANDS SECTION █ ▇ ▆ ▅ ▄ ▂ ▁#

class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,description="Kicks the given member. Please ensure both the bot and the command invoker have the permission 'Kick Members' before running this command.")
    async def kick(self, ctx, target:discord.Member):
        """Boot someone outta the server. See '+kick' for more."""
        if not str(ctx.message.channel).startswith("Direct Message with "):
            msg=await self.bot.say("Checking perms...")
            time.sleep(0.5)
            if ctx.message.server.me.server_permissions.kick_members:
                if ctx.message.author.server_permissions.kick_members:
                    await self.bot.edit_message(msg,new_content="All permissions valid, checking issues with target...")
                    time.sleep(0.5)
                    if target==ctx.message.server.owner:
                        await self.bot.edit_message(msg, new_content="All permissions are correct, but you're attempting to kick the server owner, whom you can't kick no matter how hard you try. Whoops!")
                    else:
                        if target==ctx.message.server.me:
                            await self.bot.edit_message(msg, new_content="Whoops! All permissions are correct, but you just tried to make me kick myself, which is not possible. Perhaps you meant someone else, not poor me?")
                        else:
                            await self.bot.edit_message(msg, new_content="All permissions correct, and no issues with target being self or server owner, attempting to kick.")
                            time.sleep(2)
                            try:
                                await self.bot.kick(target)
                                embed=discord.Embed(title="User Kicked!", description="**{0}** was kicked by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
                                await self.bot.say(embed=embed)
                            except Exception:
                                await self.bot.edit_message(msg, new_content="I was unable to kick the passed member. The member may have a higher role than me, I may have crashed into a rate-limit, or an unknown error may have occured. In that case, try again.")
                else:
                    await self.bot.edit_message(msg, new_content="I've the correct permissions, {}, but you do not. Perhaps ask for them?").format(ctx.message.author.mention)
            else:
                await self.bot.edit_message(msg, new_content="I'm just a poor bot with no permissions. Could you kindly grant me the permission `Kick Members`? Thanks! :slight_smile:")
        else:
            await self.bot.say("'This is a DM! This command is for servers only... try this again in a server maybe? :slight_smile:")

    @commands.command(pass_context=True,description="Bans the given member. Please ensure both the bot and the command invoker have the permission 'Ban Members' before running this command.")
    async def ban(self, ctx, target:discord.Member, days: int = 1):
        """Boot someone outta the server. See '+ban' for more."""
        if not str(ctx.message.channel).startswith("Direct Message with "):
            msg=await self.bot.say("Checking perms...")
            time.sleep(0.5)
            if ctx.message.server.me.server_permissions.ban_members:
                if ctx.message.author.server_permissions.ban_members:
                    await self.bot.edit_message(msg,new_content="All permissions valid, checking issues with target...")
                    time.sleep(0.5)
                    if target==ctx.message.server.owner:
                        await self.bot.edit_message(msg, new_content="All permissions are correct, but you're attempting to ban the server owner, whom you can't ban no matter how hard you try. Whoops!")
                    else:
                        if target==ctx.message.server.me:
                            await self.bot.edit_message(msg, new_content="Whoops! All permissions are correct, but you just tried to make me ban myself, which is not possible. Perhaps you meant someone else, not poor me?")
                        else:
                            await self.bot.edit_message(msg, new_content="All permissions correct, and no issues with target being self or server owner, attempting to ban.")
                            time.sleep(2)
                            try:
                                await self.bot.ban(target, days)
                                embed=discord.Embed(title="User Banned!", description="**{0}** was banned by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
                                await self.bot.say(embed=embed)
                            except Exception:
                                await self.bot.edit_message(msg, new_content="I was unable to ban the passed member. The member may have a higher role than me, I may have crashed into a rate-limit, or an unknown error may have occured. In that case, try again.")
                else:
                    await self.bot.edit_message(msg, new_content="I've the correct permissions, {}, but you do not. Perhaps ask for them?").format(ctx.message.author.mention)
            else:
                await self.bot.edit_message(msg, new_content="I'm just a poor bot with no permissions. Could you kindly grant me the permission `ban Members`? Thanks! :slight_smile:")
        else:
            await self.bot.say("'This is a DM! This command is for servers only... try this again in a server maybe? :slight_smile:")

    @commands.command(pass_context = True)
    async def clear(self, ctx, number):
        if ctx.message.server.me.server_permissions.manage_messages:
            if ctx.message.author.server_permissions.manage_messages:
                number = int(number) #Converting the amount of messages to delete to an integer
                counter = 0
                async for x in self.bot.logs_from(ctx.message.channel, limit = number):
                    if counter < number:
                        await self.bot.delete_message(x)
                        counter += 1
                    if counter == number:
                        msg = await self.bot.say('deleted {} messages'.format(number))
                        time.sleep(2)
                        await self.bot.delete_message(msg)

    async def update_roles(roles, server):
        if not server.id in roles:
            roles[server.id] = {}
            roles[server.id]["autorole"] = "member"

    @commands.command(pass_context=True)
    async def invite(self, ctx):
            invitelinknew = await self.bot.create_invite(destination = ctx.message.channel, xkcd = True, max_uses = 100)
            embedMsg=discord.Embed(color=0xf41af4)
            embedMsg.add_field(name="Discord Invite Link", value=invitelinknew)
            embedMsg.set_footer(text="Discord server invited link.")
            await self.bot.send_message(ctx.message.channel, embed=embedMsg)

    @commands.command(pass_context = True)
    async def mute(self, ctx, member: discord.Member):
         if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '289463060178010123':
             if not discord.utils.get(member.server.roles, name='Muted'):
                 perms = discord.Permissions(send_messages=False, read_messages=True)
                 await self.bot.create_role(ctx.message.server, name="Muted", permissions=perms)
                 role = discord.utils.get(member.server.roles, name='Muted')
                 color = cc[member.server.id]["cardcolour"]
                 colorcard = int(color)
                 embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
                 await self.bot.add_roles(member, role)
             else:
                    role = discord.utils.get(member.server.roles, name='Muted')
                    await self.bot.add_roles(member, role)
                    embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
                    await self.bot.say(embed=embed)
         else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
            await self.bot.say(embed=embed)

    @commands.command(pass_context = True)
    async def unmute(self, ctx, member: discord.Member):
         if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '289463060178010123':
           role = discord.utils.get(member.server.roles, name='Muted')
           await self.bot.remove_roles(member, role)
           embed=discord.Embed(title="User UnMuted!", description="**{0}** was unmuted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
           await self.bot.say(embed=embed)
         else:
             embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
             await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def disablelevel(self, ctx, *, member : discord.Member = None):
        if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '289463060178010123':
         with open("storage/Servers.json", "r") as f:
             servers = json.load(f)
             disable = servers[ctx.message.author.server.id]["disabled"]
             if disable == "false":
                 with open("storage/users.json","w") as w:
                    if not ctx.message.server.id in servers:
                        servers[ctx.message.server.id] = {}
                        servers[ctx.message.server.id]["disabled"] = "true"
                        json.dump(servers, w)
                        await self.bot.say("Disabled leveling system for {}".format(ctx.message.server.name))
                    else:
                        json.dump(servers, w)
                        await self.bot.say("Disabled leveling system for {}".format(ctx.message.server.name))
             elif disable == "true":
                   disable = "false"
                   with open("storage/users.json","w") as w:
                       json.dump(servers, w)
                       await self.bot.say("Enabled leveling system for {}".format(ctx.message.server.name))

def setup(bot):
    bot.add_cog(Mod(bot))
