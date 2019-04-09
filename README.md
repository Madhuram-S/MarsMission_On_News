# Use Webscrapping and build a website that will search and provide latest news on Mars NASA mission

Aim is to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.

## Step 1 - Scraping

The entire scraping is done using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

* Initial code is done usina a Jupyter Notebook file called `mission_to_mars.ipynb` and scrapes information from below websites,

### NASA Mars News

* Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

```python
# Example:
news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"

news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
```

### JPL Mars Space Images - Featured Image

* The url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) is used here.

* Use splinter to navigate the site and the image url for the current Featured Mars Image is obtained and assigned the url string to a variable called `featured_image_url`.

* It is important that image url to the full size `.jpg` image is obtained.

* Add the complete server details to relative URL path for the image to display

```python
# Example:
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
```

### Mars Weather

* From the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en), the latest Mars weather tweet is scraped from the page. The tweet text for the weather report is saved in a variable called `mars_weather`.

```python
# Example:
mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
```

### Mars Facts

* Using pandas and splinter to navigate, table containing facts about the planet including Diameter, Mass, etc., is scraped from the Mars Facts webpage [here](http://space-facts.com/mars/).

* Using Pandas the data is converted to a HTML table string.

### Mars Hemispheres

* High resolution images for each of Mar's hemispheres are obtained from the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) using splinter and beautiful soup libraries.

* The complete links to the hemispheres is saved in order to find the image url to the full resolution image.

* Both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name are saved to a dictionary. 

* Then the dictionary with the image url string and the hemisphere title is appended to a list. Thus the list will contain one dictionary for each hemisphere.

```python
# Example:
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
]
```

- - -

## Step 2 - MongoDB and Flask Application

Using MongoDB with Flask templating, a new HTML page is created that displays all of the information that was scraped from the URLs above.

* First the above Jupyter notebook is converted into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

* Next, a route called `/scrape` is created in app.py that will import your `scrape_mars.py` script and call the `scrape` function.

* The scraped information is stored in Mongo as a Python dictionary.

* A root route `/` is created that will query your Mongo database and pass the mars data into an HTML template to display the data.

* The main HTML file called `index.html` is developed that will take the mars data dictionary and display all of the data in the appropriate HTML elements. 

The following is the output of the final product

![final_app_part1.png](Images/Mars_mission_pic1.png)
![final_app_part2.png](Images/Mars_mission_pic2.png)

## Copyright

© 2019 Trilogy Education Services. All Rights Reserved.
