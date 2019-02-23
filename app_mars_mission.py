from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from mission_to_mars import scrape
import os

# Create an instance of Flask
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    db_data = mongo.db.mars_news.find_one()

        
    # Return template and data
    return render_template("index.html", marsData=db_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_data():

    # Run the scrape function and save the results to a variable
    mars_coll = mongo.db.mars_news
    mars_err_coll = mongo.db.mars_scrape_err
    scrape_status, mars_data = scrape()

    if(scrape_status['status']):
        # update only if scrape was successful
        # Update the Mongo database using update and upsert=True
        # mars_coll.update_one({}, mars_data, upsert=True)
        mars_coll.replace_one({}, mars_data, True)
    else:
        # Scrape has one or more error.. log it into a separate db collection
        mars_err_coll.replace_one({}, scrape_status, True)

        if(mongo.db.mars_news.find_one() is None):
            #use this dummy fillup data in case Mars websites are down
            mars_data_dummy = { 'scrapeStatus':'Error,serving static content','NewsDate': 'February 22, 2019',
                                 'NewsTitle': 'After a Reset, Curiosity Is Operating Normally',
                                 'News_subTitle': "NASA's Mars rover Curiosity is in good health but takes a short break while engineers diagnose why it reset its computer.",
                                 'mars_LatestImg': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23047_hires.jpg',
                                 'mars_LatestImg_desc': 'NASAs Curiosity Mars took this image with its Mastcam on Feb. 10, 2019 (Sol 2316). The rover is currently exploring a region of Mount Sharp nicknamed Glen Torridon that has lots of clay minerals.',
                                 'mars_img_thumbnail': 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA23047-640x350.jpg',
                                 'mars_img_title': 'Curiosity on the Clay Unit',
                                 'mars_latestWthr': 'InSight sol 84 (2019-02-20) low -95.1ºC (-139.2ºF) high -13.2ºC (8.3ºF) winds from the SW at 4.1 m/s (9.3 mph) gusting to 10.8 m/s (24.2 mph)',
                                 'mars_profile': '<table border="0" class="dataframe table table-striped table-hover borderless">\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>',
                                 'mars_hemis_imgs': [{'Title': 'Cerberus Hemisphere Enhanced',
                                   'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
                                  {'Title': 'Schiaparelli Hemisphere Enhanced',
                                   'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
                                  {'Title': 'Syrtis Major Hemisphere Enhanced',
                                   'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
                                  {'Title': 'Valles Marineris Hemisphere Enhanced',
                                   'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}
            mars_coll.replace_one({}, mars_data_dummy, True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
