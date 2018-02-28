from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars


@app.route("/")
def index():
    mars_content = db.mars_content.find_one()
    return render_template("index.html", mars_content=mars_content)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mars_content = db.mars_content
    mars_content.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
