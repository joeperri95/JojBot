#JojBot.py

#not for you
import secret

import discord
from discord import Game, Embed
from discord.ext.commands import Bot
import random
import datetime
import os
import sys
import time
import queue
import asyncio
import youtube_dl

BOT_PREFIX = '!'
DEBUG = "DEBUG" in [x.upper for x in sys.argv]

#for the time being
DEBUG = True

client = Bot(command_prefix=BOT_PREFIX)

#may not be necessary
ydl_opts = {
    'noplaylist' : True,
    'prefer_ffmpeg' : True
}

class bot:
    def __init__(self):
        self.connected = False
        self.connection = None
        self.musicQueue = list()
        self.currentPlayer = None

    def vc_connect(self, channel):
        if(self.isConnected()):
            return
        else:
            self.connected = True
            self.connection = channel

    def vc_disconnect(self):
        self.connected = False
        self.connection = None

    def enqueue(self, player):
        #handle input
        if(self.currentPlayer is None and not self.musicQueue):
            self.musicQueue.append(player)
            self.playNext()
        else:
            self.musicQueue.append(player)

    def dequeue(self):
        return self.musicQueue.pop(0)

    def isConnected(self):
        return self.connected

    def playNext(self):

        #if the queue is empty stop the last song
        if(not self.musicQueue):
            if(self.currentPlayer):
                self.currentPlayer.stop()
                self.currentPlayer = None
                print("Queue completed")
            return
        else:
            if(self.currentPlayer):
                self.currentPlayer.stop()
                self.currentPlayer = None
            self.currentPlayer = self.dequeue()
            print("Playing: {}".format(self.currentPlayer.title))
            self.currentPlayer.start()

    def listQueue(self):
            return [x.title for x in self.musicQueue]


b = bot()

#change to root directory
os.chdir("..")


#Commands to be used only for debugging
if(DEBUG):

    #kick jojbot from the voice channel
    @client.command(name = "vkick", brief = "this is for debugging", pass_context = True)
    async def vkick(context):
	        if(b.connection):
	                await b.connection.disconnect()
	                b.vc_disconnect()

    #testing the built in stream players
    @client.command(name = "pt", pass_context = True)
    async def pt(context):
        channel = context.message.author.voice_channel
        b = await client.join_voice_channel(channel)
        link = context.message.content.strip('!pt ')
        player = await b.create_ytdl_player(link)
        return player.start()


#8 ball command will give a response to a yes or no question
#from a tutorial may remove
@client.command(name='8ball', description = "Answer a yes/no question",
                brief = "Gives an answer to a question",
                pass_context=True)
async def eight_ball(context):
    with open("res/8BallList.txt", 'r') as fp:
        possible_responses = fp.read().split('\n')
    possible_responses = [x.strip() for x in possible_responses]
    await client.say(random.choice(possible_responses) +
                     " " + context.message.author.mention)

#give current bitcoin price
#from a tutorial may remove
#also may modify for arbitrary stock and create a nice embed
@client.command(name='bitcoin',
                description = "Get current price of bitcoin in USD",
                brief = "Get current price of bitcoin in USD")
async def bitcoin():
     url = 'http://api.coindesk.com/v1/bpi/currentprice/BTC.json'
     response = requests.get(url)
     value = response.json()['bpi']['USD']['rate']
     await client.say("Bitcoin price is " + value)

#post random image from meme folder
#should work on categories accessible from subcommands
@client.command(name="meme", description = "Get a random meme image", brief = "Grab a dank meme" , pass_context=True)
async def meme(context):
    memeList = os.listdir(os.getcwd() + "/res/Memes")
    meme = os.getcwd() + "/res/Memes/" + random.choice(memeList)

    await client.send_file(context.message.channel,meme)

#post youtube link from a list of videos about jack black
#need to use youtube api instead of this method
#youtube_dl allows for playlist use could look into that
#expand to more than this category perhaps do all kinds of MAD videos
@client.command(name="octagon", description = "Time to octagon", brief = "Get a funny video from the net", pass_context = True)
async def octagon(context):
    with open('res/OctagonList.txt' , 'r') as fp:
        videos = fp.read().split('\n')
    await client.say(random.choice(videos))

#play music from youtube link
#this is the most important feature
@client.command(name = "mus", brief = "Play a youtube link", pass_context = True)
async def mus(context):
  channel = context.message.author.voice_channel

  #kindly notify the user to join a voice channel
  if(channel is None):
    await client.say("Enter a voice channel dummy " + context.message.author.mention)
    return
  else:
    pass

  #need to handle input
  if(client.is_voice_connected(context.message.server)):
    link = context.message.content.strip('!mus ')
    try:
      player = await b.connection.create_ytdl_player(link, ytdl_options = ydl_opts, after = lambda: b.playNext())
      b.enqueue(player)

      if(DEBUG):
          print("added to the queue".format(str(player.title)))
      else:
          await client.say("{} added to the queue".format(str(player.title)))

    except CommandInvokeError:
      await client.say("That's not a valid link dawg")

  else:
    b.vc_connect(await client.join_voice_channel(channel))
    link = context.message.content.strip('!mus ')
    b.enqueue(await b.connection.create_ytdl_player(link, ytdl_options=ydl_opts, after = lambda: b.playNext()))
    print("voice connected ")

@client.command(name = "skip", brief = "next song", pass_context = True)
async def skip(context):
    if(not b.musicQueue):
        b.playNext()
        await client.say("Queue is empty")
    else:
        #need to implement an emoji instead of text here
        await client.say("DansGame")
        print("{} skipped".format(b.currentPlayer.title))
        b.currentPlayer.stop()
        #b.playNext()

#list the contents of the music queue
#need to make the embed nicer
@client.command(name = 'qlist', pass_context = True)
async def qlist(context):
    queueList = b.listQueue()
    em = Embed(title="musicQueue")

    i = 1
    for x in queueList:
        em.add_field(name = i, value = x, inline = False)
        i += 1

    await client.say("", embed = em)

@client.event
async def on_ready():
    with open(os.getcwd() + "/res/GameList.txt", "r") as gamelistfile:
        gamelist = gamelistfile.read().split('\n');
    gamechoice = random.choice(gamelist)
    await client.change_presence(game=Game(name=gamechoice))

    #dont post welcome message while in debug mode
    if(not DEBUG):
	    for server in client.servers:
	        for channel in server.channels:
	            if str(channel.type) == 'text':
                    #post welcome message in the main text channel
	                if channel.permissions_for(server.me).send_messages:
	                    if(datetime.date.today().weekday() == 2):
	                        await client.send_message(channel, "It is wednesday my dudes")
	                    else:
	                        await client.send_message(channel, "Hey paisanos")
	                    break

    print('Logged in as ' + client.user.name)

client.run(secret.TOKEN)
