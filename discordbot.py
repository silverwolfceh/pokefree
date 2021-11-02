# -*- coding: UTF-8 -*-
import requests
import random
import json
import time
import re
import socket
import discord
from discord.ext import commands
import asyncio
from pokemon import pokemon_route

#### GLOBAL VARS
DISCORD_TOKEN = "" # Put your discord token here

###

def default_route(msg):
	pass

def route(msg):
	if msg and msg.channel and msg.channel.name:
		srv = msg.guild.name
		if srv == "Pokedex100":
			pokemon_route(msg)
		else:
			default_route(msg)
####

bot = commands.Bot(command_prefix=">", description='''Selfbot by zekro''', self_bot=True)
@bot.event
async def on_message(msg):
	route(msg)

@bot.event
async def on_ready():
	print("Logged in as %s#%s" % (bot.user.name, bot.user.discriminator))
	print("ID: " + str(bot.user.id))

def discord_bot():
	try:
		bot.run(DISCORD_TOKEN, bot=False, reconnect=True)
	except Exception as e:
		print("Discord exception")
		print(e)

if __name__ == '__main__':
	discord_bot()