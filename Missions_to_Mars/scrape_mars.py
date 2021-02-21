#define a class to be called from another file
class myClass():
    #create the constructor defining the variable hemispheres
    def __init__(self,dicti,hemispheres,texto3,t_html,textoTitle):
        self.dicti=dicti
        self.hemispheres=hemispheres
        self.texto3=texto3
        self.t_html=t_html
        self.textoTitle=textoTitle
        
    #create the function that runs the Mars scraping script
    def scrape(self,dicti,hemispheres,texto3,t_html,textoTitle):
    # Dependencies

        from bs4 import BeautifulSoup as bs
        import requests
        import pandas as pd
        from selenium.webdriver import Chrome
        from selenium.webdriver.support.ui import Select
        from selenium import webdriver

        #telling the Chrome driver where is the executable
        driver = Chrome(executable_path='C:/Webdriver/bin/chromedriver')


        #defining a string variable with the website url
        url = "https://mars.nasa.gov/news/"

        #Making a connection to the Nasa News website
        r = requests.get(url)

        #creating a soup object with the html data
        soup = bs(r.text, 'lxml')

        #Finding all the div tags in the soup
        texto=soup.find_all('div')

        # Opening the website
        driver.get(url)


        # getting the button by class name
        button = driver.find_element_by_class_name("menu_icon")


        # clicking on the button
        button.click()

        #Defining a button for a reactive element which matches the request
        button = driver.find_element_by_id("li_4")


        #click the button
        button.click()

        #saving the current url to a variable for automation
        url2=driver.current_url
        url2

        #Connecting with the News and Events website
        r2=requests.get(url2)

        #creating a soup object with the html text from the Mars Nasa website news and events
        soup2 = bs(r2.text, 'lxml')

        #Looking for all the news and then selecting only the latest news 
        texto2=soup2.find_all('h3', class_="title")
        textoTitle=texto2[0].text.strip()

        #defining the button content (reactive link) for the first news
        button=driver.find_element_by_class_name('list_image')

        #clicking button 
        button.click()

        #Checking the url of the redirected website. Saving to a variable
        url3=driver.current_url
        url3

        #connect to the website that contains the main news
        r3=requests.get(url3)

        #create a soup object for this website
        soup3=bs(r3.text,'lxml')

        #This is the first paragraph of the main text of these news
        texto3=soup3.find('p')
        texto3

        #define a variable with the string of the Space facts website
        url4='https://space-facts.com/mars/'

        #Using requests to connect to Space Facts website
        r4=requests.get(url4)

        #creating a soup element for this website (Mars Facts)
        soup4=bs(r4.text,'lxml')

        #extracting html from website
        texto4=soup4.find('table')
        #texto4

        #reading the html table from the website Mars Facts
        table=pd.read_html(url4)
        table[0]

        #cresting a dataframe with the information extracted from Mars Facts
        df=pd.DataFrame(table[0])
        df.rename(columns = {0:'Property', 1:'Value'}, inplace = True)
        df

        #Converting the Mars facts to html code
        t_html=pd.DataFrame.to_html(df)
        #t_html

        driver.implicitly_wait(10)

        #website for the hemisphere images of Mars
        url5='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        #executing the driver to automatically go to the website
        driver.get(url5)

        url5=driver.current_url
        r5=requests.get(url5, timeout=10)
        print(r5)

        #Create a beautiful soup element with the the html 
        main=bs(r5.text,'lxml')
        titles=main.find_all('div', class_='description')
        #titles

        #collecting the titles of the various images
        titlist=[]

        try:
            for tit in titles:
                tititem=tit.find('h3').text
                titlist.append(tititem)

        except:
            print("Something went wrong")
            print(titlist)

        #including a wait for these websites because the response is not fast
        driver.implicitly_wait(10)

        #getting the references from the html script
        elems = driver.find_elements_by_css_selector(".description [href]")
        links = [elem.get_attribute('href') for elem in elems]
        links

        def but1(tag,links,driver):
            urln=links[tag]
            driver.get(urln)
            button=driver.find_element_by_link_text("Sample")
            button.click()
            urlimg=driver.current_url
            return urlimg
        
        
        #Extracting the links to the images from the website (these are not the downloadable ones)
        urlimg=[]
        for u in range(4):
            addurl=but1(u,links,driver)
            urlimg.append(addurl)

        #print(urlimg)

        #assigning a variable to the Mars images website
        url6='https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'

        #testing the response of the website
        r6=requests.get(url6, timeout=10)
        r6

        #inspecting the dataframe for images
        pd.DataFrame({titlist[i]: links[i] for i in range(len(links))}, index=[0])

        #hemispheres=[]
        
        # saving a list of dictionaries with Mars images information
        for i in range(4):
            dic={"Hemisphere":titlist[i], "Image":links[i]}
            hemispheres.append(dic)

        driver.close()
        #print(hemispheres)
        return hemispheres, texto3,t_html,textoTitle

