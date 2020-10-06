from kvdb import kvdb

class userpref:
	__instance = None
	def __init__(self):
		self.pref = "PREF_"
		self.noti = "NOTI_ME"
		self.teleid = "TELE_"
		self.listkey = []
		self.__init_instance()

	def __init_instance(self):
		if userpref.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			userpref.__instance = self

	@staticmethod
	def get_instance():
		if userpref.__instance == None:
			userpref()
		return userpref.__instance

	def _db_check_add(self, k, newv):
		v = kvdb.get_instance().get(k)
		if v == False:
			kvdb.get_instance().set(k,[newv])
		elif newv in v:
			pass
		else:
			v.append(newv)
			kvdb.get_instance().set(k,v)

	def _db_remove(self, k, chk):
		v = kvdb.get_instance().get(k)
		if v == False:
			pass
		elif chk in v:
			v.remove(chk)
			kvdb.get_instance().set(k,v)
		else:
			pass

	def uid_has_noti(self, uid):
		v = kvdb.get_instance().get(self.noti)
		if uid in v:
			return True
		return False

	def on_noti(self, uid):
		self._db_check_add(self.noti, uid)

	def off_noti(self, uid):
		self._db_remove(self.noti, uid)


	def on_pref(self, pkname, uid):
		k = "%s%s"%(self.pref, pkname)
		self._db_check_add(k, uid)
		k = "%s%s"%(self.teleid, uid)
		self._db_check_add(k, pkname)

	def get_pref(self, pkname):
		k = "%s%s"%(self.pref, pkname)
		v = kvdb.get_instance().get(k)
		if v == False:
			return []
		else:
			return v

	def get_pref_by_uid(self, uid):
		k = "%s%s"%(self.teleid, uid)
		v = kvdb.get_instance().get(k)
		if v == False:
			return []
		else:
			return v

	def off_pref(self, pkname, uid):
		k = "%s%s"%(self.pref, pkname)
		self._db_remove(k, uid)
		k = "%s%s"%(self.teleid, uid)
		self._db_remove(k, pkname)

	def uid_has_pref(self, pkname, uid):
		k = "%s%s"%(self.pref, pkname)
		v = kvdb.get_instance().get(k)
		if uid in v:
			return True
		return False