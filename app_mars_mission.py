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
        mars_coll.update({}, mars_data, upsert=True)
    else:
        # Scrape has one or more error.. log it into a separate db collection
        mars_err_coll.update({}, scrape_status, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
