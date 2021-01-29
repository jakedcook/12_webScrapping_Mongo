from flask import Flask, render_template, redirect
import pymongo
import scrape
from scrape import scrape_all
import os


app = Flask(__name__)

conn = 'mongodb://localhost:27017'
mongo = pymongo.MongoClient(conn)

@app.route('/')
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route('/scrp')
def scrp():
    mars_info = mongo.db.mars_info
    mars_meta = scrape.scrape_all()
    mars_info.update({}, mars_meta, upsert=True)

    return redirect('/', code=302)




if __name__ == '__main__':
    app.run(debug=True)