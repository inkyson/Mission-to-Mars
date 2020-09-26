from flask import Flask, render_template # use Flask to render a template
from flask_pymongo import PyMongo # use PyMongo to interact with Mongo database
import scraping # to use scraping code, convert Jupyter notebook to Python

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define route for the HTML page
@app.route("/") # tells Flask what to display when we're looking at the homepage
def index(): # index.html is the default HTML file that we'll use to display the dontent we've scraped
    mars = mongo.db.mars.find_one() # uses PyMongo to find the mars collection in our database. assign that path to mars variable to use later
    return render_template("index.html", mars=mars) # tells Flask to return an HTML template using an index.html file. Use mars collection in MongoDB

@app.route("/scrape") # defines the route that Flask will be using
def scrape(): # scrapes new data using our scraping.py script
    mars = mongo.db.mars # assign a new variable that points to our Mongo database
    mars_data = scraping.scrape_all() # create a new variable to hold the newly scraped data
    mars.update({}, mars_data, upsert=True) # update the database.  syntax .update(query_parameter, data, options) upsert tells Mongo to create a new document if it doesn't exist already.
    return "Scraping Successful!"

# Run flask
if __name__ == "__main__":
    app.run()