# -*- coding: UTF-8 -*-
from pokedex100 import PokeDex100
from telegrambot import telegrambot
from recentpokemon import *
import json
import requests

RARE_LIST_DEFAULT = ["togetic", "unown", "dragonite", "tyranita", "scyther", "lapras"]

def parse_ok_cb(data):
	detail = data["detail"]
	pname = detail["name"]
	region_detector = pname.split(" ")[0]
	if region_detector == "Alolan":
		pname = pname.split(" ")[1]
	if pname.lower() in telegrambot.get_rare_poke() or int(detail["L"]) >= 30 or int(detail["cp"]) >= 2500:
		print(detail)
		new_url = "https://pokefree.silverwolfceh.repl.co/showdata?code=%s" % detail["urlcode"]
		save_pokemon(detail)
		telegram_fmt = "%s CP%s L%s URL: %s | SHOW: %s" % (detail["name"], detail["cp"], detail["L"],detail["url"], new_url)
		if detail["shiny"]:
			telegram_fmt = "**" + telegram_fmt
		telegrambot.sendMessage("@tongvuu", telegram_fmt)
	else:
		print("Pokemon %s not sastify the condition" % detail["name"] )

def parse_err_cb(data):
	pass

def pokemon_route(msg):
	cname = msg.channel.name
	if cname.startswith("level30community") or cname.startswith("unown") or cname.startswith("100iv_"):
		ins = PokeDex100.getInstance()
		ins.parse(msg, parse_ok_cb, parse_err_cb)

def reveal_cords(url):
	ins = PokeDex100.getInstance()
	return ins.reveal_cords(url)
