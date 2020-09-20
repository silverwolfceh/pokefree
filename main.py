from threading import Thread
from flask import Flask, render_template, request, url_for
import requests
import json
import re
import urllib
import sys
from bs4 import BeautifulSoup
from telegrambot import *
from discordbot import *
from pokemon import reveal_cords

app = Flask("SimpleBot")
app.config["DEBUG"] = False


@app.route("/telegrambot", methods=["POST", "GET"])
def telegrambot_handle():
	if request.method == "POST":
		postdata = request.data
		bot = telegrambot(postdata)
		bot.handle()
	return ""

@app.route("/posttome", methods=["POST", "GET"])
def post_to_me():
  if request.method == "GET":
    data = request.args.get("message")
  else:
    data = request.data
  #telegrambot.sendMessage("706061752", data)
  telegrambot.sendMessage("@tongvuu", data)
  return "OK"

@app.route("/revealcoords", methods=["GET"])
def revealcoords():
	data = request.args.get("url")
	return reveal_cords(data)

@app.route("/ping", methods=["GET"])
def keepalive():
	return "PONG"

@app.route("/")
def form():
	return render_template('index.html')
def run_flash():
	app.run(host='0.0.0.0', debug=False)

if __name__ == "__main__":
	Thread(target=run_flash).start()
	discord_bot()
	#app.run(host='0.0.0.0', debug=True)