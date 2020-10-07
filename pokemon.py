# -*- coding: UTF-8 -*-
from pokedex100 import PokeDex100
from telegrambot import telegrambot
from recentpokemon import save_pokemon
from userpref import userpref

RARE_LIST_DEFAULT = ["togetic", "unown", "dragonite", "tyranita", "scyther", "lapras"]

def parse_ok_cb(data):
	detail = data["detail"]
	pname = detail["name"]
	region_detector = pname.split(" ")[0]
	if region_detector == "Alolan":
		pname = pname.split(" ")[1]

	# Prepare poke data
	new_url = "https://pokefree.silverwolfceh.repl.co/showdata?code=%s" % detail["urlcode"]
	telegram_fmt = "%s CP%s L%s URL: %s | SHOW: %s" % (detail["name"], detail["cp"], detail["L"],detail["url"], new_url)
	if detail["shiny"]:
		telegram_fmt = "**" + telegram_fmt
	poke_saved = False


	# Find if any user interested in pokemon
	uids = userpref.get_instance().get_pref(pname.lower())
	for usr in uids:
		if poke_saved == False:
			save_pokemon(detail)
			poke_saved = True
		if userpref.get_instance().uid_has_noti(usr):
			telegrambot.sendMessage(usr, telegram_fmt)

	# Channel evaluation
	if pname.lower() in telegrambot.get_rare_poke() or int(detail["L"]) >= 30 or int(detail["cp"]) >= 2500:
		if poke_saved == False:
			save_pokemon(detail)
			poke_saved = True
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
