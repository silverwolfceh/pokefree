# -*- coding: UTF-8 -*-
import requests
class PokeDex100(object):
	__instance = None
	def __init__(self):
		self.discord_msg = None
		self.msg = ""
		self.cookie = { "csrftoken": "ynoZVNW0ugkgtRUiRW567Iz1QVQZjR4lWdk7zYdCCzaC72WKeRL3lOkroiBqDDIH", "sessionid" : "3zz2sz7n0xtqkbyibrhz022j3hl6z4a1" }
		if PokeDex100.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			PokeDex100.__instance = self

	def _get_pokeNAME(self):
		s = self.msg.find("**")
		e = self.msg.find("**", s + 1)
		if s == -1 or e == -1:
			print("Failed to process pokemon")
			return self.msg
		pname = self.msg[s + 2 : e]
		return pname

	def _get_pokeCP(self):
		s = self.msg.find("CP")
		e = self.msg.find("**", s + 1)
		cp = "???"
		if s != -1 and e != -1:
			cp = self.msg[s + 2 : e]
		return cp

	def _get_pokeLVL(self):
		s = self.msg.find("** **L")
		e = self.msg.find("**", s + 6)
		level = "???"
		if s != -1 and e != -1:
			level = self.msg[s + 6 : e]
		return level

	def _parse_poke_data(self):
		name = self._get_pokeNAME()
		cp = self._get_pokeCP()
		level = self._get_pokeLVL()
		return name,cp,level
		

	def _get_url(self):
		embeds = self.discord_msg.embeds
		for embed in embeds:
			raw = str(embed.fields[0])
			s = raw.find("/free=")
			e = raw.find(")", s + 1)
			if s == -1 or e == -1:
				print("Failed to get url")
				return ""
			url = raw[s + 6 : e]
			return url
		print("Failed to find url")
		return ""


	def parse(self, discord_msg, success_cb, failed_cb):
		self.discord_msg = discord_msg
		self.msg = discord_msg.content.split("\n")[0]
		name,cp,level = self._parse_poke_data()
		url = self._get_url()
		if url == "":
			data = {"code" : "ng", "detail" : "failed to parse data"}
			failed_cb("Parse error for pokemon")
			return False
		else:
			data = {"code" : "ok", "detail" : {"name" : name, "cp" : cp, "L" : level, "url" : "http://api.pokedex100.com/discord/free=%s" % url, "urlcode" : url}}
			success_cb(data)
			return True

	def reveal_cords(self, url):
		r = requests.get(url, cookies=self.cookie)
		res = r.text
		s_text = 'type="text" value="'
		s = res.find(s_text)
		e = res.find('" id="', s + 5)
		if s == -1 or e == -1:
			print("Failed to get coords")
			return ""
		coords = res[s+len(s_text): e]
		return coords

	@staticmethod 
	def getInstance():
		if PokeDex100.__instance == None:
			PokeDex100()
		return PokeDex100.__instance
