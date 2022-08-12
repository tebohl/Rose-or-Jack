# import necessary libraries
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        feature1 = request.form["feature1"]
        feature2 = request.form["feature2"]
        feature3 = request.form["feature2"]

        pet = Pet(feature1=feature1, feature2=feature2, feature3=feature3)
        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")



if __name__ == "__main__":
    app.run()

