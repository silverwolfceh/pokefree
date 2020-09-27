from replit import db

class ringdb:
	def __init__(self, num_key, key_prefix):
		self.idx = 0
		self.LIMIT = num_key
		self.PREFIX = key_prefix

	def save(self, data):
		if self.idx >= self.LIMIT:
			self.idx = 0
		db["%s%s" % (self.PREFIX, str(self.idx))] = data
		self.idx = self.idx + 1

	def find_by(self, var, varstr):
		for i in range(0, self.LIMIT):
			try:
				data = db["%s%s" % (self.PREFIX, str(i))]
				if data[varstr] == var:
					return data
			except:
				pass
		return []

	def get(self, idx):
		if idx < LIMIT and idx > 0:
			try:
				data = db["%s%s" % (self.PREFIX, str(idx))]
			except:
				print("Not found data at index")
				return []
		else:
			print("Index out of range")
			return []