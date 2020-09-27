from ringdb import ringdb

POKE_PREFIX = "POKEDATA_"
POKE_LIMIT = 100
poke_db_inst = None


def save_pokemon(data):
	global poke_db_inst
	if not poke_db_inst:
		poke_db_inst = ringdb(POKE_LIMIT, POKE_PREFIX)
	poke_db_inst.save(data)


def find_by_url_code(urlcode):
	global poke_db_inst
	if not poke_db_inst:
		poke_db_inst = ringdb(POKE_LIMIT, POKE_PREFIX)
		return []
	else:
		data = poke_db_inst.find_by(urlcode, "urlcode")