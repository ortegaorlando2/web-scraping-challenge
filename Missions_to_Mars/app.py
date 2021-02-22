# Import Flask
from flask import Flask, render_template, redirect
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
#Import my scraping class
import scrape_mars
from scrape_mars import myClass
 

# Create an instance of our Flask app.
app = Flask(__name__)

#Get image for decoration from Activities folder Extra Content
# _________________________________________________________
from bs4 import BeautifulSoup
from splinter import Browser
executable_path = {"executable_path": 'C:/Webdriver/bin/chromedriver'}
browser = Browser("chrome", **executable_path, headless=False)
url = "https://en.wikipedia.org/wiki/Mars"
browser.visit(url)
xpath = '//td//a[@class="image"]/img'
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()

url2 = browser.html
soup = BeautifulSoup(url2, 'html.parser')
img_url_temp1 = soup.find("tbody").find('a', class_='image')['href']
img_url_temp=f'https://en.m.wikipedia.org/{img_url_temp1}'
print(img_url_temp)

browser.visit(img_url_temp)
url3= browser.html
soup2= BeautifulSoup(url3, "html.parser")
img_url_file= soup2.find("div", class_='fullImageLink').find('a')['href']
img_url=f'https:{img_url_file}'
print(img_url)

import requests
import shutil
response = requests.get(img_url, stream=True)
with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
from IPython.display import Image 
Decor=Image(url='img.png')

browser.quit()
#______________________________________________________________________


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
MarsPhotos=db.MarsPhotos
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
# scrape_mars.myClass.scrape(dicti,hemispheres,title3)

# def scrape():
#     instance=myClass.scrape(dicti,hemispheres,texto3)
#     print(texto3)
#     return render_template("index.html", News=texto3)

# print(instance)


@app.route("/scrape")
# dicti={}
# hemispheres=[]
def scraper():
    #Photos_data={}
    MarsPhotos = db.MarsPhotos
    class_instance =scrape_mars.myClass(dicti,hemispheres,texto3,t_html,textoTitle)
    class_instance.scrape(dicti,hemispheres,texto3,t_html,textoTitle)
    print(hemispheres)
    print(texto3)
    for i in hemispheres:
        MarsPhotos.insert_one(i.Hemisphere)
        MarsPhotos.insert_one(i.Image)
    return redirect("/", code=302) 

db.HemImages.insert_many(
[{'Hemisphere':'Cerberus Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, 
    {'Hemisphere':'Schiaparelli Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
     {'Hemisphere':'Syrtis Major Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, 
     {'Hemisphere':'Valles Marineris Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]
)

db.Facts1.insert_one({"Fact":'Equatorial Diameter=	', 'Value':'6,792 km'})
db.Facts1.insert_one({"Fact":'Polar Diameter= ','Value':'6,752 km'})
db.Facts1.insert_one({"Fact":'Mass= ', 'Value':'6.39 × 10^23 kg (0.11 Earths)'})
db.Facts1.insert_one({"Fact":'Moons= ','Value':'6.39 × 10^23 kg (0.11 Earths)'})
db.Facts1.insert_one({"Fact":'Orbit Distance= ','Value':'2 (Phobos & Deimos)'})
db.Facts2.insert_one({"Fact":'Orbit Period= ','Value':'687 days (1.9 years)'})
db.Facts2.insert_one({"Fact":'Surface Temperature= ','Value':'-87 to -5 °C'})
db.Facts2.insert_one({"Fact":'First Record: ','Value':'2nd millennium BC'})
db.Facts2.insert_one({"Fact":'Recorded By: ','Value':'Egyptian astronomers'})

#mongo = PyMongo(app, uri="mongodb://localhost:27017/MarsPhotos")

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
    Decor=Image(url='img.png')
    News=texto3
    OneHemisphere=""#mongo.db.HemImages.find_one_or_404()
    return render_template('index.html', MarsPhotos=MarsPhotos, MarsFacts1=MarsFacts1, MarsFacts2=MarsFacts2, 
    OneHemisphere=OneHemisphere, News=News, img_url=img_url)

   

if __name__ == "__main__":
    app.run(debug=True)
