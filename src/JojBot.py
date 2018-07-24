#run.py

#JojBot discord bot

BOT_PREFIX = '!'

#not for you
import secret

import discord
from discord import Game
from discord.ext.commands import Bot
import random
import os
import queue

class bot:
	def __init__(self):
		self.connected = False
		self.connection = None
		self.musicQueue = queue.Queue()
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
		self.musicQueue.put(player)

	def dequeue(self):
		return self.musicQueue.get()

	def isConnected(self):
		return self.connected

	def playNext(self):
		player = self.musicQueue.get()
		player.play()


b = bot()


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

@client.command(name = "mus", pass_context = True)
async def mus(context):
  channel = context.message.author.voice_channel
  if(channel is None):
  	await client.say("Enter a voice channel dummy " + context.message.author.mention)
  	return
  else:
  	pass

  if(b.isConnected()):
  	link = context.message.content.strip('!mus ')
  	player = await b.connection.create_ytdl_player(link, after = lambda: b.playNext())
  	b.enqueue(player)
  	await client.say("I enqueued it b")
  	pass
  
  else:
  	b.vc_connect(await client.join_voice_channel(channel))
  	link = context.message.content.strip('!mus ')
  	b.enqueue(await b.connection.create_ytdl_player(link, after = lambda: b.playNext()))
  	b.dequeue().start()

@client.event
async def on_ready():
    with open(os.getcwd() + "/res/GameList.txt", "r") as gamelistfile:
        gamelist = gamelistfile.read().split('\n');
    gamechoice = random.choice(gamelist)
    await client.change_presence(game=Game(name=gamechoice))
    print('Logged in as ' + client.user.name)

client.run(secret.TOKEN)