from threading import Thread
from flask import Flask, render_template, request, url_for
import requests
import json
import time
import re
import urllib
import sys
sys.path.append("/Library/Python/3.7/site-packages")
from bs4 import BeautifulSoup
from telegrambot import *
from discordbot import *
from recentpokemon import *
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

@app.route("/showpokes", methods=["GET"])
def show_current_rare_list():
	rlist = telegrambot.get_rare_poke()
	return "<br />".join(rlist)

@app.route("/showdata", methods=["GET"])
def show_poke_data_from_code():
	code = request.args.get("code")
	data = find_by_url_code(code)
	if len(data) == 0:
		return "Failed to find related data"
	else:
		coord = reveal_cords("http://api.pokedex100.com/discord/free=" + code)
		if coord == "":
			return "Failed to reveal coord"
		else:
			msg = "%s CP%s LVL%s <br /> %s" %(data["name"], data["cp"], data["L"], coord)
			return msg



@app.route("/posttome", methods=["POST", "GET"])
def post_to_me():
  if request.method == "GET":
    data = request.args.get("message")
  else:
    data = request.data
  telegrambot.sendMessage("706061752", data)
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

def db_maintain():
	while True:
		handle_rare_list_db()
		time.sleep(5)

if __name__ == "__main__":
	Thread(target=run_flash).start()
	Thread(target=db_maintain).start()
	discord_bot()