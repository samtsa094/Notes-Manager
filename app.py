from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import datetime
import os
load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGOURI", "mongodb://localhost:27017/notes_manager")
app.config["SECRET_KEY"] = os.getenv("SECRETKEY") or os.urandom(32)
mongo = PyMongo(app)
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        notes = mongo.db.Notes.find()
        return render_template("index.html", notes = notes)
@app.route("/delete/<note_id>")
def delete(note_id):
    mongo.db.Notes.delete_one({"_id": ObjectId(note_id)})
    return redirect("/")
@app.route("/add", methods = ["POST"])
def add():
    print(request.form)
    document = {}
    document["note"] = request.form.get("note")
    document["timestamp"] = datetime.datetime.now()
    mongo.db.Notes.insert_one(document)
    return redirect("/")
if __name__ == "__main__":
    app.run(debug = True)