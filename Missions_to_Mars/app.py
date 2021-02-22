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
#_________________________________________________________
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
MarsFacts1=db.MarsFacts1
MarsFacts2=db.MarsFacts2
MarsPhotos=db.MarsPhotos

# Drops collection if available to remove duplicates
db.HemImages.drop()
db.MarsFacts1.drop()
db.MarsFacts2.drop()
db.MarsPhotos.drop()

#Initialize remote class variables
dicti={"":""}
hemispheres=[]
textoTitle=""
texto3=""
t_html=""
#______________________________________________________________________

#run remote class and method to obtain data scraped from websites
# scrape_mars.myClass.scrape(dicti,hemispheres,title3)

# def scrape():
#     instance=myClass.scrape(dicti,hemispheres,texto3)
#     print(texto3)
#     return render_template("index.html", News=texto3)

# print(instance)


#Retrieving all results from remote class
myclass=myClass(dicti,hemispheres,texto3,t_html,textoTitle)
hemispheres,texto3,t_html,textoTitle = myclass.scrape(hemispheres,texto3,t_html,textoTitle)

print(hemispheres,texto3,t_html,textoTitle)

Title=textoTitle
paragraph=texto3

#making a dictionary with the latest News from Mars
News = {'Title':textoTitle, "paragraph":texto3}          
MarsFacts1.insert_one(News)

HemImages.insert_one(hemispheres)

# Facts={"Table":t_html}
# MarsFacts2.insert_one(Facts)



print(HemImages)

#______________________________________________________________________
# running the remote class inside an app
@app.route("/scrape")
# dicti={}
# hemispheres=[]
def scraper():
    # #Photos_data={}
    # HemImages=db.HemImages
    # Facts1=db.Facts1
    # Facts2=db.Facts2
    # MarsPhotos = db.MarsPhotos
    # #class_instance =myclass(dicti,hemispheres,texto3,t_html,textoTitle)
    # myclass.scrape(dicti,hemispheres,texto3,t_html,textoTitle)
    # #print(hemispheres)
    # #print(texto3)
    # Facts2.insert_one({'News':textoTitle})
    # Facts2.insert_one({'paragraph':texto3})
    # Facts1.insert_one({'Mars_Facts':t_html})
    # #for i in hemispheres:
    # MarsPhotos.update({}, )

    for i in hemispheres:
    # Error handling
        try:

            hemispheres = hemispheres
            if (hemispheres):
            # Print results
                print('-------------')

            item={i}
            HemImages.insert_one(item)
        # Imageurl = f'{hemispheres["Image"]}'
        # browser.visit(Imageurl)
        # Image(url=f'{i.Image}.png')

        except Exception as e:
            print(e) 

    return redirect("/", code=302) 
#______________________________________________________________________

# IF EVERYTHIN GOES WONG 
# db.HemImages.insert_many(
# [{'Hemisphere':'Cerberus Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, 
#     {'Hemisphere':'Schiaparelli Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
#      {'Hemisphere':'Syrtis Major Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, 
#      {'Hemisphere':'Valles Marineris Hemisphere', 'Image':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]
# )

db.MarsFacts2.insert_one({"Fact":'Equatorial Diameter=	', 'Value':'6,792 km'})
db.MarsFacts2.insert_one({"Fact":'Polar Diameter= ','Value':'6,752 km'})
db.MarsFacts2.insert_one({"Fact":'Mass= ', 'Value':'6.39 × 10^23 kg (0.11 Earths)'})
db.MarsFacts2.insert_one({"Fact":'Moons= ','Value':'6.39 × 10^23 kg (0.11 Earths)'})
db.MarsFacts2.insert_one({"Fact":'Orbit Distance= ','Value':'2 (Phobos & Deimos)'})
db.MarsFacts2.insert_one({"Fact":'Orbit Period= ','Value':'687 days (1.9 years)'})
db.MarsFacts2.insert_one({"Fact":'Surface Temperature= ','Value':'-87 to -5 °C'})
db.MarsFacts2.insert_one({"Fact":'First Record: ','Value':'2nd millennium BC'})
db.MarsFacts2.insert_one({"Fact":'Recorded By: ','Value':'Egyptian astronomers'})

#______________________________________________________________________
# Set route to index.html to display data
@app.route('/')
def index():
    # Store the collection in a list
    MarsPhotos = list(db.HemImages.find())
    # Store the collection in a list
    MarsFacts1 = list(db.MarsFacts1.find())
    News=MarsFacts1[0]['Title']
    print(MarsFacts1)
    # News = MarsFacts1.Title
    # paragraph = paragraph
    # Store the collection in a list
    MarsFacts2 = list(db.MarsFacts2.find())
    # Return the template with the items passed in

    return render_template('index.html', MarsPhotos=MarsPhotos, News=News, img_url=img_url, paragraph=paragraph, Table=MarsFacts2)

   

if __name__ == "__main__":
    app.run(debug=True)
