import requests
import json
import nextcord
import hanging
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

start_msg = "Welcome USER"
start_cmd = "hangman"
start_runnig = "USER is already playing hangman"

guess_cmd = "guess"

resposne1 = "You can choose language with command '!choose LANGUAGE'"

playing = {}

@bot.command()
async def start(ctx, *, msg=None):
    global playing
    
    if not str(ctx.author.id) in playing:
        if msg.lower() == start_cmd:
            new_msg = start_msg.replace("USER", ctx.author.mention)
            new_msg += '\n'+resposne1
        
            for language in languages:
                new_msg += '\n'+language.upper()

            word = requests.get(generator_url).json()

            playing[str(ctx.author.id)] = {
                'lives' : 7,
                'untranslated' : word[0],
                'language' : None,
                'translated' : None,
                'hidden' : "",
                'letters' : []
            }

            print("untranslated word is ", playing[str(ctx.author.id)]['untranslated'])

            return await ctx.send(new_msg)
    elif msg == None or msg.lower() != start_cmd:
        new_msg = ctx.author.mention+" send invalid message"

        return await ctx.send(new_msg)

    if msg.lower() == start_cmd:
        new_msg = start_runnig.replace("USER", ctx.author.mention)

        await ctx.send(new_msg)

@bot.command()
async def choose(ctx, *, msg=None):
    global playing

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
        print("lan", msg.lower())

        playing[str(ctx.author.id)]['language'] = msg.lower()
        
        taal = playing[str(ctx.author.id)]['language']

        woord = playing[str(ctx.author.id)]['untranslated']
        translated = None

        if playing[str(ctx.author.id)]['language'] == "en":
            playing[str(ctx.author.id)]['translated'] = woord

            translated = playing[str(ctx.author.id)]['translated']
        else:
            translated = translators.google(woord, 'auto', taal)
            
            playing[str(ctx.author.id)]['translated'] = translated
        
        hiddenword = ""

        for i in range(len(translated.strip())):
            hiddenword += "🔴 "

        playing[str(ctx.author.id)]['hidden'] = hiddenword

        await ctx.send(ctx.author.mention+" starting hangman in: "+msg.upper())
        await ctx.send("guess word: "+playing[str(ctx.author.id)]['hidden'])

@bot.command()
async def guess(ctx, *, msg=None):
    global playing

    msg_strip = msg.strip()

    if not str(ctx.author.id) in playing:
        return
    elif playing[str(ctx.author.id)]['language'] == None:
        return await ctx.send(ctx.author.mention+" hasn't chosen a language yet\nuse command '!choose LANGUAGE'")
    elif msg == None or msg.lower() in playing[str(ctx.author.id)]['letters']:
        return await ctx.send(ctx.author.mention+" has already geussed letter: "+msg.lower())
    elif len(msg_strip) != 1:
        return await ctx.send(ctx.author.mention+" message either contains spaces or is not a letter")
    
    translated = playing[str(ctx.author.id)]['translated']
    geussed_letters = playing[str(ctx.author.id)]['letters']

    print(translated)
    
    if msg.lower() in translated.lower():
        geussed_letters.append(msg.lower())

        await ctx.send("letter "+msg.upper()+" is in word")
    else:
        playing[str(ctx.author.id)]['lives'] -= 1

        lives = playing[str(ctx.author.id)]['lives']

        geussed_letters.append(msg.lower())

        await ctx.send(msg.upper()+" is not in word\n"+hanging.hanging[lives])
    
    if playing[str(ctx.author.id)]['lives'] == 0:
        del playing[str(ctx.author.id)]

        await ctx.send("your word was "+translated)

@bot.command()
async def steps(ctx):
    intro_str = "Hallo, "+ctx.author.mention
    intro_str += "\n1. To begin Hangman use command '!start hangman'"
    intro_str += "\n2. Use command '!choose LANGUAGE' to choose your preffered language"
    intro_str += "\n3. Use command '!guess LETTER' to guess a letter"
    intro_str += "\n4. Now enjoy :)"
    
    await ctx.send(intro_str)
    

@bot.event
async def on_ready():
    print("ready")

bot.run(token)