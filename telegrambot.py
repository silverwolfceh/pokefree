import requests
import urllib
import json
import os
from pokedex100 import PokeDex100
from kvdb import kvdb
from userpref import userpref

BOT_TOKEN="" # Put the telegram bot token here
BOT_URL= "https://api.telegram.org/bot%s" % BOT_TOKEN
AUTHOR = "@darksoulxx"
RARE_LIST_KEY = "POKERARE"
RARE_LIST_DEFAULT = ["togetic", "unown", "dragonite", "tyranita", "scyther", "lapras"]
DB_PLAUSI = []

class telegrambot:
	__instance = None
	def __init__(self, dbroot = None):
		self.rxdata = []
		self.simple_callback = {
			"/author" 		: self.handleAuthor,
			"/donate" 		: self.handleDonate,
			"/help" 		: self.handleHelp,
			"/test" 		: self.handleTest,
			"/me"			: self.handleUserId,
			"/id2phone"		: self.handleIdToPhone,
			"/showpokes"    : self.showPokemonsInRareList,
			"/notion"       : self.handleNotifyOn,
			"/notioff"      : self.handleNotifyOff,
			"/getpgsharp"   : self.handlePGSharpKey
		}

		self.param_callback = {
			"/poke"			: self.handlePokedex,
			"/addpokes"     : self.addPokemonsToRareList,
			"/delpokes"     : self.deletePokemonsFromRareList,
			"/favpokes"     : self.handleUserFavoritePoke,
			"/addpgsharp"   : self.handlePGSharpUpdate
			
		}

		self.multi_state_callback = {

		}

		self.is_message = True
		self._init_instance()
		#self.parse()
		
	def _init_instance(self):
		if telegrambot.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			telegrambot.__instance = self

	@staticmethod 
	def get_instance():
		if telegrambot.__instance == None:
			telegrambot()
		return telegrambot.__instance

	def parse(self, data):
		self.rxdata = data
		req = json.loads(self.rxdata)
		if "message" not in req:
			self.is_message = False
		else:
			self.fromid = req["message"]["from"]["id"]
			self.chatid = req["message"]["chat"]["id"]
			self.chatmsg = req["message"]["text"]
			self.fromname = req["message"]["from"]["first_name"]
			self.msg = req["message"]
		return self

	def handle(self):
		if self.is_message:
			cmd = self.chatmsg.split(" ")
			if cmd[0] in self.simple_callback:
				self.simple_callback[self.chatmsg]()
			elif cmd[0] in self.param_callback:
				self.param_callback[cmd[0]](cmd)
			else:
				self.simple_callback["/help"]()
		else:
			# It is not a message from user
			pass

	def get_db(self, key):
		v = kvdb.get_instance().get(key)
		if v == False:
			self.set_db(key, [])
			return []
		return v

	def set_db(self, key, val):
		return kvdb.get_instance().set(key, val)
		

	@staticmethod
	def get_rare_poke():
		v = kvdb.get_instance().get(RARE_LIST_KEY)
		if v == False:
			kvdb.get_instance().set(RARE_LIST_KEY, [])
			return []
		return v

	# PARAM CALLBACK
	def handlePGSharpUpdate(self, cmd):
		pass
	def handleUserFavoritePoke(self, cmd):
		if len(cmd) < 2:
			self.reply("Syntax: /favpokes add/del/show poke1 poke2")
			return
		support_ops = ["add", "del", "show"]
		ops = cmd[1]
		if ops not in support_ops:
			self.reply("Syntax: /favpokes add/del/show poke1 poke2")
			return
		if ops == "add":
			for i in range(2, len(cmd)):
				poke = cmd[i]
				userpref.get_instance().on_pref(poke.lower(), self.fromid)
			self.reply("OK")
		elif ops == "del":
			for i in range(2, len(cmd)):
				poke = cmd[i]
				userpref.get_instance().off_pref(poke.lower(), self.fromid)
			self.reply("OK")
		elif ops == "show":
			vlist = userpref.get_instance().get_pref_by_uid(self.fromid)
			self.reply("OK. Check here")
			self.reply('\n'.join(vlist))
		else:
			self.reply("Something really WRONG happen")
			return

		pass
	def addPokemonsToRareList(self, cmd):
		if len(cmd) <= 1:
			self.reply("You need to specifid pokemon name")
			return
		added_poke = ""
		rlist = self.get_db(RARE_LIST_KEY)
		for i in range(1, len(cmd)):
			if cmd[i].lower() not in rlist:
				rlist.append(cmd[i].lower())
				added_poke = added_poke + cmd[i] + " "
			else:
				pass
		self.set_db(RARE_LIST_KEY, rlist)
		self.reply("OK. Add %s" % added_poke)

	def deletePokemonsFromRareList(self, cmd):
		if len(cmd) <= 1:
			self.reply("You need to specifid pokemon name")
			return
		deleted_poke = ""
		rlist = self.get_db(RARE_LIST_KEY)
		for i in range(1, len(cmd)):
			if cmd[i].lower() in rlist:
				rlist.remove(cmd[i].lower())
				deleted_poke = deleted_poke + cmd[i] + " "
			else:
				pass
		self.set_db(RARE_LIST_KEY, rlist)
		self.reply("OK. Deleted %s" % deleted_poke)

	def handlePokedex(self, cmd):
		if len(cmd) <= 1:
			self.reply("Wrong syntax")
			return
		url = cmd[1]
		if url.startswith("http://api.pokedex100.com/discord"):
			ins = PokeDex100.getInstance()
			coords = ins.reveal_cords(url)
			if coords != "":
				self.reply("OK. Here is your coords")
				self.reply(coords)
			else:
				self.reply("Sorry, we can't reveal your link")
		else:
			self.reply("Sorry, your request is wrong")


	# SIMPLE CALLBACK
	def handlePGSharpKey(self):
		self.reply("Hello %s, thanks for visitting us" % self.fromname)
		pass

	def handleNotifyOn(self):
		userpref.get_instance().on_noti(self.fromid)
		self.reply("OK. Notification has been enabled")
	
	def handleNotifyOff(self):
		userpref.get_instance().off_noti(self.fromid)
		self.reply("OK. Turn off notification. If you want on, send /notion")

	def handleUserId(self):
		self.reply("Your user id: " + str(self.fromid))

	def handleAuthor(self):
		self.reply("Author: %s" % AUTHOR)
	
	def handleIdToPhone(self):
		pass
	
	def handleDonate(self):
		self.reply("Paypal: silverwolf@ceh.vn")
		self.reply("Momo : 0903417427")
		self.reply("If you want donate others, please PM %s. Thank you" % AUTHOR)

	def handleHelp(self):
		self.reply("Hello, this is an auto bot to answer to commands")
		self.handleAuthor()

	def showPokemonsInRareList(self):
		rlist = self.get_db(RARE_LIST_KEY)
		self.reply("OK, Here are pokemon in your DB")
		self.reply('\n'.join(rlist))
		pass

	# Bot functions
	def reply(self, txmsg):
		url = "%s/sendMessage?chat_id=%s&text=%s&disable_web_page_preview=true" % (BOT_URL, str(self.chatid), (txmsg))
		requests.get(url)

	def handleTest(self, data = None):
		self.reply("PING...PONG")

	@staticmethod
	def sendMessage(to_id, msg):
		url = "%s/sendMessage?chat_id=%s&text=%s&disable_web_page_preview=true" % (BOT_URL, to_id, msg)
		requests.get(url)


def handle_rare_list_db():
	global DB_PLAUSI, RARE_LIST_DEFAULT, RARE_LIST_KEY
	rare_list = telegrambot.get_rare_poke()
	if len(rare_list) == 0: #DB is empty
		print("DB has not initlize or was wipped")
		if len(DB_PLAUSI) == 0:
			kvdb.get_instance().set(RARE_LIST_KEY, RARE_LIST_DEFAULT)
		else:
			kvdb.get_instance().set(RARE_LIST_KEY, DB_PLAUSI)
	else:
		DB_PLAUSI = rare_list

