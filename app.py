# import necessary libraries
from pickle import load
import numpy as np
from flask import Flask, render_template, request

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Load ML Model
#################################################
model = load(open('./models/model_randomforrest_2022080848.pkl', 'rb'))

# create route that renders index.html template
@app.route("/")
def home():

    # # Method 1 inputs
    # pclass = ""
    # name = ""
    # sex = ""
    # age = ""
    # family = ""
    # ticket = ""
    # fare = ""
    # embarked = ""

    prediction_text = ""

    return render_template("index.html", result = prediction_text)


# Query the database and send the jsonified results
@app.route("/send", methods=["POST"])
def send():

    # # Method 1:  Obtain form inputs and add to numpy array or dataframe
    # pclass = request.form["survivedpclass"]
    # name = request.form["survivedname"]
    # sex = request.form["survivedsex"]
    # age = request.form["survivedage"]
    # family = request.form['survivedfamily']
    # ticket = request.form['survivedticket']
    # fare = request.form['survivedfare']
    # embarked = request.form['survivedembarked']

    # Method 2:  Obtain form inputs and add to numpy array   
    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]

    # use form results to make prediction
    prediction = model.predict(final_features)[0]

    # create html content - either single variable, dictionary, or string
    prediction_text = f"Your fate: {(prediction)}."

    # send prediction to html page
    return render_template("index.html", result = prediction_text)


if __name__ == "__main__":
    app.run()
