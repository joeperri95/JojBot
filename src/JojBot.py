#JojBot discord bot

BOT_PREFIX = '!'

#not for you
import secret

import discord
from discord import Game
from discord.ext.commands import Bot
import random
import os
import requests
import queue

#change to root directory
os.chdir("..")

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball', description = "Answer a yes/no question",
                brief = "Gives an answer to a question",
                pass_context=True)
async def eight_ball(context):
    with open("res/8BallList.txt", 'r') as fp:
        possible_responses = fp.read().split('\n')
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

@client.command(name = "music", pass_context = True)
async def music(context, link):
    pass
    
    

@client.command(name="meme", description = "Get a random meme image", brief = "Grab a dank meme" , pass_context=True)
async def meme(context):
    memeList = os.listdir(os.getcwd() + "/res/Memes")
    meme = os.getcwd() + "/" + random.choice(memeList)
    
    await client.send_file(context.message.channel,meme)

@client.command(name="octagon", description = "Time to octagon", brief = "Get a funny video from the net", pass_context = True)
async def octagon(context):
    with open('res/OctagonList.txt' , 'r') as fp:
        videos = fp.read().split('\n')
    await client.say(random.choice(videos))

@client.event
async def on_ready():
    with open(os.getcwd() + "/res/GameList.txt", "r") as gamelistfile:
        gamelist = gamelistfile.read().split('\n');
    gamechoice = random.choice(gamelist)
    await client.change_presence(game=Game(name=gamechoice))
    await client.send_message(discord.Object('342738319819407370') , "Guess who's back")
    print('Logged in as ' + client.user.name)    

client.run(secret.TOKEN)


