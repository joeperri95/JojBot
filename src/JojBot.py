#JojBot discord chatbot

BOT_PREFIX = '!'

import secrets
import discord
from discord import Game
from discord.ext.commands import Bot
import random
import os
import requests

#change to root directory
os.chdir("..")

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball', description = "Answer a yes/no question",
                brief = "Gives an answer to a question",
                pass_context=True)
async def eight_ball(context):
    with open("8BallList.txt", r) as fp:
      possible_responses = fp.readlines()    
    possible_responses = [x.strip() for x in possible_responses]
    await client.say(random.choice(possible_responses) +
                     " " + context.message.author.mention)

@client.command(name='bitcoin',
                description = "Get current price of bitcoin in USD",
                brief = "Get current price of bitcoin in USD")
async def bitcoin():
     url = 'http://api.coindesk.com/v1/bpi/currentprice/BTC.json'
     response = requests.get(url)
     value = response.json()['bpi']['USD']['rate']
     await client.say("Bitcoin price is " + value)

@client.command(name="meme", description = "Get a random meme image", brief = "Grab a dank meme" , pass_context=True)
async def meme(context):
    memeList = os.listdir(os.getcwd() + "/res/Memes")
    meme = os.getcwd() + "/" + random.choice(memeList)
    
    await client.send_file(context.message.channel,meme)

@client.event
async def on_ready():
    gamelistfile = open(os.getcwd() + "/res/GameList.txt", "r")
    gamelist = gamelistfile.read().split('\n');
    gamechoice = random.choice(gamelist)
    await client.change_presence(game=Game(name=gamechoice))
    print('Logged in as ' + client.user.name)
    gamelistfile.close()

client.run(TOKEN)


