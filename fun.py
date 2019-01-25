import discord
from discord.ext import commands
import os
import time
import random
from random import choice
from time import perf_counter
from pyshorteners import Shortener
import aiohttp
import asyncio
import datetime
import json
import re
import praw
from cogs.utils.dataIO.dataIO import js


class Fun:
    def __init__(self, bot):
        with open("data/useful/settings.json", "r") as g:
            self.bot = bot
            self.settings = json.load(g)

    @commands.command(pass_context=True, name="ping", aliases=['pong'])
    async def _ping(self, ctx):
        """Pong!"""
        t1 = perf_counter()
        await self.bot.send_typing(ctx.message.channel)
        t2 = perf_counter()
        time = str((t2 - t1) * 1000) # converting to milliseconds.
        t1 = time.split(".")[0]      # everything before the dot is needed.
        t2 = time.split(".")[1][:2]  # only 2 decimals behind the dot.
        await self.bot.say("Pong! Response time: **{} ms**.".format(t1 + "." + t2))

    @commands.command(pass_context=True, name="avatar", aliases=["av"])
    async def avatar(self, ctx, user : discord.Member):
        if user.avatar_url:
            avatar = user.avatar_url
        else:
            avatar = user.default_avatar_url
        em = discord.Embed(color=discord.Color.red())
        em.add_field(name=user.mention + "'s avatar", value=avatar)
        em.set_image(url=avatar)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, name="calc", aliases=["calculate"])
    async def _calc(self, ctx, evaluation):
        """Solves a math problem so you don't have to!
        + = add, - = subtract, * = multiply, and / = divide
        Example:
        [p]calc 1+1+3*4"""
        prob = re.sub("[^0-9+-/* ]", "", ctx.message.content[len(ctx.prefix + ctx.command.name) + 1:].strip())
        if len(evaluation) > 64:
            await self.bot.say("That evalution is too big, I can allow a maximum of 64 characters, I suggest you divide it in smaller portions.")
            return
        try:
            answer = str(eval(prob))
            await self.bot.say("`{}` = `{}`".format(prob, answer))
        except:
            await self.bot.say("I couldn't solve that problem, it's too hard.")

    @commands.command(pass_context=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def bugreport(self, ctx, *, bug:str):
        with open("data/useful/settings.json", "r") as g:
            self.settings = js.load("data/useful/settings.json")
            """Report a bug in the bot."""
            if self.settings.owner == "289463060178010123":
                await self.bot.say("I have no owner set, cannot report the bug.")
                return
                owner = discord.utils.get(self.bot.get_all_members(), id=self.settings.owner)
                author = ctx.message.author
                if ctx.message.channel.is_private is False:
                    server = ctx.message.server
                    source = "server **{}** ({})".format(server.name, server.id)
                else:
                    source = "direct message"
                    sender = "**{0}** ({0.id}) sent you a bug report from {1}:\n\n".format(author, source)
                    message = sender + bug
                    try:
                        await self.bot.send_message(owner, message)
                    except discord.errors.InvalidArgument:
                        await self.bot.say("I cannot send your bug report, I'm unable to find my owner... *sigh*")
                    except discord.errors.HTTPException:
                        await self.bot.say("Your bug report is too long.")
                    except:
                        await self.bot.say("I'm unable to deliver your bug report. Sorry.")
                    else:
                        await self.bot.say("Your bug report has been sent.")

    @commands.command(pass_context=True)
    async def fortune(self, ctx, member : discord.Member = None):
        if not member == None:
            """This will tell you a fortune"""
            randomlist = ['{} will be a millionare'.format(member),'{} will eat baguette'.format(member),'{} will die lonely'.format(member),'{} will be famous'.format(member),'{} will be a cool boi/girl'.format(member)]
            embed=discord.Embed(title="Fortune", description=random.choice(randomlist), color=0xff00f6)
            await self.bot.say(embed=embed)
        else:
            """This will tell you a fortune"""
            randomlist = ['You will be a millionare','You will eat baguette','You will die lonely','You will be famous','You will be a cool boi/girl']
            embed=discord.Embed(title="Fortune", description=random.choice(randomlist), color=0xff00f6)
            await self.bot.say(embed=embed)


    @commands.command(pass_context=True)
    async def hug(self, ctx, *, member : discord.Member = None):
        """Maybe you want to hug a friend?"""
        if member is None:
                embed=discord.Embed(title="Hug", description=ctx.message.author.mention + " has been hugged!", color=0xff00f6)
                await self.bot.say(embed=embed)
        else:
            if member.id == ctx.message.author.id:
                embed=discord.Embed(title="Hug", description=ctx.message.author.mention + " hugged themselves(you might want to hug them back, they seem lonely)", color=0xff00f6)
                await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Hug", description=member.mention + " has been hugged by " + ctx.message.author.mention + "!", color=0xff00f6)
                await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def choice(self, ctx, *, choices: str):
        """This can be helpful to choose something for you, if you dont know what to choose"""
        choicesArr = choices.split(",")
        chosen = choicesArr[random.randrange(len(choicesArr))]
        embed=discord.Embed(title="Choice", description=ctx.message.author.mention + ": i choose " + chosen, color=0xff00f6)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def level(self, ctx, *, member : discord.Member = None):
        """Show yours or a users level"""
        with open("storage/users.json", "r") as f:
            users = json.load(f)
            experience = users[ctx.message.author.id + "-" + ctx.message.server.id]["experience"]
            lvl_start = users[ctx.message.author.id + "-" + ctx.message.server.id]["level"]
            lvl_end = int(experience ** (1/4))
            if member is None:
                embed=discord.Embed(title="User Level", description=f"You are level {lvl_start} and have {experience} xp!", color=0xff00f6)
                await self.bot.say(embed=embed)
            else:
                if member.id == ctx.message.author.id:
                    embed=discord.Embed(title="User Level", description=f"You are level {lvl_start} and have {experience} xp!", color=0xff00f6)
                    await self.bot.say(embed=embed)
                else:
                    lvl_start2 = users[member.id + "-" + ctx.message.server.id]["level"]
                    xp2 = users[member.id + "-" + ctx.message.server.id]["experience"]
                    embed=discord.Embed(title="User Level", description=f"{member} is level {lvl_start2} and have {xp2} xp!", color=0xff00f6)
                    await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        #embed=discord.Embed(description="These are the available commands", color=0x0080ff, timestamp=datetime.datetime.utcfromtimestamp(1548091066))
        #embed.set_author(name="Baguette Bot", url="https://media.discordapp.net/attachments/444140244179353610/536854888244707328/image0.png?width=450&height=450", icon_url="https://media.discordapp.net/attachments/444140244179353610/536854888244707328/image0.png?width=450&height=450")
        #embed.set_thumbnail(url="https://media.discordapp.net/attachments/444140244179353610/536854888244707328/image0.png?width=450&height=450")
        #embed.add_field(name="Help", value="`Help Command.`", inline=True)
        #embed.add_field(name="level", value="`Shows a players level.`", inline=False)
        #embed.add_field(name="fortune", value="`Tells you a fortune.`", inline=False)
        #embed.add_field(name="hug", value="`Hug someone.`", inline=False)
        #embed.add_field(name="choice", value="`The bot can choose things for you.`", inline=False)
        #embed.add_field(name="calculate", value="`The bot can calculate things for you.`", inline=False)
        #embed.add_field(name="quickpoll", value="`Makes a poll.`", inline=False)
        #embed.add_field(name="embed", value="`Use +embed for more info.`", inline=False)
        #embed.add_field(name="translate", value="`Translate into a given language (doesnt work everytime) use +langlist for list of languages.`", inline=False)
        #embed.set_footer(text="Help command")
        #await self.bot.send_message(ctx.message.author, embed=embed)
        embed = discord.Embed(title = 'Help', description = 'These are all the bot-commands!', color = 0xffffff, timestamp=datetime.datetime.now())
        embed.add_field(name = 'help' , value = 'The command you just used.', inline = True)
        embed.add_field(name = 'helpmod'  , value = 'For moderation commands.', inline = True)
        await self.bot.send_message(ctx.message.author, embed=embed)
        await self.bot.say('{} i sent you a dm with my commands!.format(ctx.message.author.mention))
        embed = discord.Embed(title = 'Useful Commands', description = 'These are very useful commands!', color = 0x00a800, timestamp=datetime.datetime.now())
        embed.add_field(name = 'about' , value = 'Gives you more information on the bot.', inline = False)
        embed.add_field(name = 'calculate' , value = 'When you are too lazy to calculate things yourself.', inline = False)
        embed.add_field(name = 'choice' , value = 'The bot will choose for you. Example: (+choice "Budbot will eat pancakes" "Budbot will eat cookies"', inline = False)
        embed.add_field(name = 'quickpoll' , value = 'Make a very quick poll! Example:(+quickpoll "Is Budbot a good bot?" yes no) you can also add custom anwsers: (+quickpoll "Is Budbot a good bot?" "Maybe." "Very Yes." "Ill ask my cat."'), inline = False)
        embed.add_field(name = 'embed' , value = 'Embed a message! Use +embed for more info!', inline = False)
        embed.add_field(name = 'translate' , value = 'You can speak every language now! Example: (+translate [language (like : "en" or "de")] [what you want to translate]) Use "+translate langlist" to view the supported languages.)', inline = False)
        await self.bot.send_message(ctx.message.author, embed=embed)

        embed = discord.Embed(title = 'Fun commands', description = 'These are very fun commands!', color = 0xa80000, timestamp=datetime.datetime.now())
        embed.add_field(name = '(NEW) randomfact' , value = 'For your daily random knowledge.', inline = False)
        embed.add_field(name = 'level' , value = 'Shows your level.', inline = False)
        embed.add_field(name = 'fortune' , value = 'If you want Budbot to predict your future.', inline = False)
        embed.add_field(name = 'hug' , value = 'Give people a hug.', inline = False)
        embed.add_field(name = 'meme' , value = 'For your daily memes.', inline = False)
        embed.set_footer(text = 'Help Command')
        await self.bot.send_message(ctx.message.author, embed=embed)
    @commands.command(pass_context=True)
    async def ownertest(self, ctx):
        if ctx.message.author.id == "289463060178010123":
            embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~", colour=discord.Colour(0xe6a28d), url="https://discordapp.com", description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```", timestamp=datetime.datetime.utcfromtimestamp(1548091066))

            embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_author(name="author name", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

            embed.add_field(name="🤔", value="some of these properties have certain limits...")
            embed.add_field(name="😱", value="try exceeding some of them!")
            embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
            embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
            embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

            await self.bot.say(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)
        else:
            self.bot.say("Ehm how do you know this command? Oh well only the owner can use it")

    @commands.command(pass_context=True)
    async def meme(self, ctx):
        reddit = praw.Reddit(client_id='VUbJvq1yQQ5YpQ',
                     client_secret='usu3jomlfPmHDGY-iYob0bBrvl8',
                     user_agent='your mom')
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await self.bot.say(submission.url)

    @commands.command(pass_context=True)
    async def baguette(self, ctx):
        reddit = praw.Reddit(client_id='VUbJvq1yQQ5YpQ',
                     client_secret='usu3jomlfPmHDGY-iYob0bBrvl8',
                     user_agent='your mom')
        memes_submissions = reddit.subreddit('BaguetteConnect').hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await self.bot.say(submission.url)

def check_folders():
    if not os.path.exists("data/useful"):
        print("Creating data/useful folder...")
        os.makedirs("data/useful")

def check_files():
    if not os.path.exists("data/useful/settings.json"):
        print("Creating data/useful/settings.json file...")
        for data in os.listdir(".\\data/useful"):
            os.save_json("data/useful/settings.json", {'auth_key': 'key_here', 'client_id': 'client_id_here', 'geocodingkey': 'key_here', 'timezonekey': 'key_here'})
            print("Saved data")

def setup(bot):
    check_folders()
    check_files()
    bot.remove_command('help')
    bot.add_cog(Fun(bot))
