import requests
import json
import nextcord
from nextcord.ext import commands
from languages import *

with open('token.txt') as file:
    token = file.read()

intents = nextcord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents
)

with open('url.txt') as file:
    generator_url = file.read()

word = requests.get(generator_url).json()

start_msg = "Welcome USER"
start_cmd = "hangman"
start_runnig = "USER is already playing hangman"

resposne1 = "You can choose language with command '!choose LANGUAGE'"

playing = []

@bot.command()
async def start(ctx, *, msg=None):
    if not str(ctx.author.id) in playing:
        if msg.lower() == start_cmd:
            new_msg = start_msg.replace("USER", ctx.author.mention)
            new_msg += '\n'+resposne1
        
            for language in languages:
                new_msg += '\n'+language

            playing.append(str(ctx.author.id))

            return await ctx.send(new_msg)
    elif msg == None or msg.lower() != start_cmd:
        new_msg = ctx.author.mention+" send invalid message"

        return await ctx.send(new_msg)

    if msg.lower() == start_cmd:
        new_msg = start_runnig.replace("USER", ctx.author.mention)

        await ctx.send(new_msg)

@bot.command()
async def choose(ctx, *, msg=None):
    if not str(ctx.author.id) in playing:
        new_string = "USER hasn't started hangman yet or choose an invalid language"

        new_msg = new_string.replace("USER", ctx.author.mention)
        new_msg += "\nuse the '!start hangman' command to begin playing"

        return await ctx.send(new_msg)
    elif msg == None or not msg.lower() in languages:
        new_string = "USER "+msg+" is not a valid language"

        new_msg = new_string.replace("USER", ctx.author.mention)

        playing.remove(str(ctx.author.id))

        return await ctx.send(new_msg)

    if msg.lower() in languages:
        await ctx.send(ctx.author.mention+" starting hangman in: "+msg.upper())

@bot.event
async def on_ready():
    print("ready")

bot.run(token)