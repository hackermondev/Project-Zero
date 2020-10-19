from replit import db

def set(name, value):
	db[name] = value

def get(name):
	try:
		v = db[name]
		return v
	except KeyError:
		return None

def delete(name):
	del db[name]

def delete_all():
    for i in db.keys():
        del db[i]
    return True

def get_all():
	return db.keys()