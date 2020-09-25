from replit import db

POKE_KEY_PRE = "POKEDATA_"
POKE_LIMIT = 100
POKE_IDX = 0

def save_pokemon(data):
	global POKE_IDX, POKE_LIMIT, POKE_KEY_PRE
	if POKE_IDX >= POKE_LIMIT:
		POKE_IDX = 0
	db[POKE_KEY_PRE + str(POKE_IDX)] = data
	POKE_IDX = POKE_IDX + 1

def find_by(var, varstr):
	global POKE_IDX, POKE_LIMIT, POKE_KEY_PRE
	for i in range(0, POKE_LIMIT):
		try:
			data = db[POKE_KEY_PRE + str(i)]
			if data[varstr] == var:
				return data
		except:
			pass
	return []

def find_by_url_code(urlcode):
	return find_by(urlcode, "urlcode")

def find_by_first_poke(pokename):
	return find_by(pokename, "name")

