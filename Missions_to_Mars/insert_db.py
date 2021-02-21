from pymongo import MongoClient

# connect to mongo
mongodb_url = 'mongodb://localhost:27017'
mongo_client = MongoClient(mongodb_url)

# get handle to mongo db and create collection
mongo_db = mongo_client.MarsPhotos_db
collection = mongo_db.Facts

# function to insert data into players collection
def insert_facts_in_db():
    facts_lst = [
        {'Equatorial Diameter:	':'6,792 km'},
        {'Polar Diameter: ':'6,752 km'},
        {'Mass ':'6.39 × 10^23 kg (0.11 Earths)'},
        {'Moons ':'6.39 × 10^23 kg (0.11 Earths)'},
        {'Orbit Distance ':'2 (Phobos & Deimos)'},
        {'Orbit Period ':'687 days (1.9 years)'},
        {'Surface Temperature ':'-87 to -5 °C'},
        {'First Record ':'2nd millennium BC'},
        {'Recorded By ':'Egyptian astronomers'}
    ]
    collection.insert_many(facts_lst)
    return

if __name__ == '__main__':
    # insert data in db
    insert_facts_in_db()