import pickledb

class kvdb:
	__instance = None
	def __init__(self):
		self.db = pickledb.load('database.db', True, False)
		self.__init_instance()

	def __init_instance(self):
		if kvdb.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			kvdb.__instance = self

	def __del__(self):
		self.db.dump()

	def set(self, k, v):
		return self.db.set(k, v)

	def get(self, k):
		return self.db.get(k)

	@staticmethod
	def get_instance():
		if kvdb.__instance == None:
			kvdb()
		return kvdb.__instance

