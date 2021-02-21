# Import Flask
from flask import Flask, render_template
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
from pymongo import MongoClient
#Import my scraping class
import scrape_mars
from scrape_mars import myClass

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.MarsPhotos_db
#Mars_collection that will contain the data
HemImages=db.HemImages
Facts1=db.Facts1
Facts2=db.Facts2
# Drops collection if available to remove duplicates
db.HemImages.drop()
db.Facts1.drop()
db.Facts2.drop()
#Initialize some variables
dicti={"":""}
hemispheres=[]
textoTitle=""
texto3=""
t_html=""

#run remote class and method to obtain data scraped from websites
# f=myClass.scrape(dicti,hemispheres)
# print(f)

#temporarilly defining the dictionary until the websites respond
#function to insert Photos data into collection

@app.route("/scrape")
# dicti={}
# hemispheres=[]
def scraper():
    dicti={}
    hemispheres=[]
    MarsPhotos = db.MarsPhotos_db.HemImages
    Photos_data = scrape_mars.myClass.scrape(dicti,hemispheres)
    MarsPhotos.insert_many(Photos_data)
    return redirect("/", code=302) 

# db.HemImages.insert_many(
# [{'Hemisphere':'Cerberus Hemisphere Enhanced', 'Image':'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'}, 
#     {'Hemisphere':'Schiaparelli Hemisphere Enhanced', 'Image':'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'},
#      {'Hemisphere':'Syrtis Major Hemisphere Enhanced', 'Image':'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'}, 
#      {'Hemisphere':'Valles Marineris Hemisphere Enhanced', 'Image':'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'}]
# )

db.Facts1.insert_one({"Fact":'Equatorial Diameter=	', 'Value':'6,792 km'})
db.Facts1.insert_one({"Fact":'Polar Diameter= ','Value':'6,752 km'})
db.Facts1.insert_one({"Fact":'Mass= ', 'Value':'6.39 × 10^23 kg (0.11 Earths)'})
db.Facts1.insert_one({"Fact":'Moons= ','Value':'6.39 × 10^23 kg (0.11 Earths)'})
db.Facts1.insert_one({"Fact":'Orbit Distance= ','Value':'2 (Phobos & Deimos)'})

db.Facts2.insert_one({"Fact":'Orbit Period= ','Value':'687 days (1.9 years)'})
db.Facts2.insert_one({"Fact":'Surface Temperature= ','Value':'-87 to -5 °C'})
db.Facts2.insert_one({"Fact":'First Record: ','Value':'2nd millennium BC'})
db.Facts2.insert_one({"Fact":'Recorded By: ','Value':'Egyptian astronomers'})


# Set route
@app.route('/')
def index():
    # Store the collection in a list
    MarsPhotos = list(db.HemImages.find())
    # Store the collection in a list
    MarsFacts1 = list(db.Facts1.find())
    # Store the collection in a list
    MarsFacts2 = list(db.Facts2.find())
    # Return the template with the items passed in
    return render_template('index.html', MarsPhotos=MarsPhotos, MarsFacts1=MarsFacts1, MarsFacts2=MarsFacts2,)

   

if __name__ == "__main__":
    app.run(debug=True)
