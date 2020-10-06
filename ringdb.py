from kvdb import kvdb

class ringdb:
	def __init__(self, num_key, key_prefix):
		self.idx = 0
		self.LIMIT = num_key
		self.PREFIX = key_prefix

	def _setdb(self, k,v):
		return kvdb.get_instance().set(k, v)
	
	def _getdb(self, k):
		return kvdb.get_instance().get(k)

	def save(self, data):
		if self.idx >= self.LIMIT:
			self.idx = 0
		#db["%s%s" % (self.PREFIX, str(self.idx))] = data
		self._setdb("%s%s" % (self.PREFIX, str(self.idx)), data)
		self.idx = self.idx + 1

	def find_by(self, var, varstr):
		for i in range(0, self.LIMIT):
			try:
				#data = db["%s%s" % (self.PREFIX, str(i))]
				data = self._getdb("%s%s" % (self.PREFIX, str(i)))
				if data[varstr] == var:
					return data
			except:
				pass
		return []

	def get(self, idx):
		if idx < self.LIMIT and idx > 0:
			try:
				#data = db["%s%s" % (self.PREFIX, str(idx))]
				data = self._getdb("%s%s" % (self.PREFIX, str(idx)))
				return data
			except:
				print("Not found data at index")
				return []
		else:
			print("Index out of range")
			return []