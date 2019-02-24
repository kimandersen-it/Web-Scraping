# Dependencies
import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


# Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/)
# URL of page to be scraped

url = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'html.parser')
# print(soup.prettify())
results = soup.find_all('div', class_="slide")
# print(results)
all_titles = []
all_desc = []

for result in results:

    try:

        title = result.find('div', class_="content_title").a.text
        all_titles.append(title)

        desc = result.find('div', class_="rollover_description_inner").text
        all_desc.append(desc)

        # print("title and descriptions are :")
    #  print("-----------------------------")
    #  if(title and desc):

    #   print(title)
    #   print(desc)

    except AttributeError as e:
        print(e)

first_title = all_titles[0].strip()
print(first_title[0:])

first_desc = all_desc[0].strip()
print(first_desc[0:])

# URL of page to be scraped

url = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
twresponse = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
twsoup = bs(twresponse.text, 'html.parser')

# print(soup.prettify())
twresults = twsoup.find_all('div', class_="content")

all_weath = []



for twresult in twresults:
    try:

        weather = twresult.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        all_weath.append(weather)


    except AttributeError as e:
        print(e)

first_weath = all_weath[0].strip()

# Below from Saturday Class
# u'Sol 2319 (2019-02-13), high -17C/1F, low -72C/-97F, pressure at 8.12 hPa, daylight 06:46-18:52pic.twitter.com/anlHR95BMs'

# URL of page to be scraped

url = 'https://space-facts.com/mars/'

# Retrieve page with the requests module
facresponse = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
facsoup = bs(facresponse.text, 'html.parser')

#print(facsoup.prettify())

facresults = facsoup.find_all('div', class_="post-content")

# Mars Facts
facresponse = requests.get("https://space-facts.com/mars/")
facsoup = bs(facresponse.content,'lxml')
factable = facsoup.find_all('table')[0]
factfinal = pd.read_html(str(factable))

#factfinal

url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
# Retrieve page with the requests module
hemresponse = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
hemsoup = bs(hemresponse.text, 'html.parser')

# print(hemsoup.prettify())

hemimages = [
    {"title": "Cerberus Hemisphere Enhanced",
     "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"},
    {"title": "Schiaparelli Hemisphere Enhanced",
     "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"},
    {"title": "Syrtis Major Hemisphere Enhanced",
     "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"},
    {"title": "Valles Marineris Hemisphere Enhanced",
     "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"}

    ]

# Flask

# hemimages
from flask import Flask, render_template

import pymongo

# Create an instance of flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database.
db = client.mars_db

# make sure it doesn't already exist
db.mars.drop()
#

# create collection
db.mars.insert_many(
    [


        {"fact":"Equatorial Diameter -  6,792 km"},
        {"fact":"Polar Diameter -  6,752 km"},
        {"fact":"Mass - 6.42 x 10^23 kg (10.7% Earth)"}

      
    ]
)



                 #   },
                 #   'Image Files': {
                 #       "Cerberus": [hemimages[0]],
                 #       "Schiaparelli": [hemimages[1]],
                 #       "Syrtis Major": [hemimages[2]],
                  #      "Valles Marineris": [hemimages[3]]
                  #  }




# Set route
@app.route('/')
def index ():
    # store the mars info
    mars = list(db.mars.find())
    print(mars)

    # Return the template
    return render_template('index_mars.html', mars=mars)


if __name__ == "__main__":
    app.run(debug=True)
