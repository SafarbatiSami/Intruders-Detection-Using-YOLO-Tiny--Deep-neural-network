from flask import Flask, render_template_string
from flask import render_template
from flask_pymongo import PyMongo
from bson import ObjectId
import base64

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sam:rfid@cluster0.dt27d.mongodb.net/AItruders?retryWrites=true&w=majority"
mongo = PyMongo(app)
print("Connected to MongoDB Atlas!")

@app.route("/workers")
def get_images():
    image_docs = mongo.db.Workers.find({}, {"picture": 1, "Time": 1})
    images = []
    for doc in image_docs:
        encoded_image = base64.b64encode(doc["picture"]).decode("utf-8")
        images.append({"image": encoded_image, "time": doc["Time"]})
    
    # Render the HTML template with the <img> tags for all images
   
    #return render_template_string(html_template, images=images)
    return render_template('workers.html', images=images)


@app.route("/intruders")
def get_imagess():
    image_docs = mongo.db.Intruders.find({}, {"picture": 1, "Time": 1})
    images = []
    for doc in image_docs:
        encoded_image = base64.b64encode(doc["picture"]).decode("utf-8")
        images.append({"image": encoded_image, "time": doc["Time"]})
    return render_template('intruders.html', images=images)



@app.route("/")
def HomeRoute():
    image_docs = mongo.db.Intruders.find({}, {"picture": 1, "Time": 1})
    images = []
    for doc in image_docs:
        encoded_image = base64.b64encode(doc["picture"]).decode("utf-8")
        images.append({"image": encoded_image, "time": doc["Time"]})
    return render_template('index.html', images=images)


if __name__ == "__main__":
    app.run()
 

 
