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
model = load(open('model_randomforrest_2022080848.pkl', 'rb'))
# load the scaler
scaler = load(open('scaler.pkl', 'rb'))

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visual")
def visual():
    return render_template("visualizations.html")

@app.route("/models")
def models():
    return render_template("models.html")

# create route that renders index.html template
@app.route("/form")
def form():

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

    return render_template("predictor.html", result = prediction_text)

# Query the database and send the jsonified results
@app.route("/send", methods=["POST"])
def send():
    firstclass= 0
    secondclass= 0
    thirdclass= 0
    male= 0
    female= 0
    # # Method 1:  Obtain form inputs and add to numpy array or dataframe
    age = float(request.form["survivedage"])
    fare = float(request.form['survivedfare'])
    converted_fare = fare/154
    family = float(request.form['survivedfamily'])
    if fare < 1000:
        pclass = "3"
        thirdclass=1
    elif fare < 2500:
        pclass = "2"
        secondclass=1
    else:
        pclass = "1"
        firstclass = 1
    # pclass = request.form["survivedpclass"]
    # if pclass == "1":
    #     firstclass= 1
    # elif pclass == "2":
    #     secondclass= 1
    # else:
    #     thirdclass= 1
    sex = request.form["survivedsex"]
    if sex == "Male":
        male= 1
    else:
        female= 1

    features= [age, converted_fare, family, firstclass, secondclass, thirdclass, female, male]

    
    # transform the test dataset
    final_features = [np.array(features)]
    features_scaled = scaler.transform(final_features)
    

    # Method 2:  Obtain form inputs and add to numpy array   
    # features = [float(x) for x in request.form.values()]
    # final_features = [np.array(features)]

    # # use form results to make prediction
    prediction = model.predict(features_scaled)[0]

    # create html content - either single variable, dictionary, or string
    if prediction == 1: 
        prediction_text = "Congratulations! You survived!"
    else:
        prediction_text = "Game Over - No room for you on the raft."
    display_form_input = f"You are a {(int(age))} year old {(sex)}, traveling with {int((family))} family members. You paid ${(fare)} to travel in {(pclass)}st class."

    # send prediction to html page
    return render_template("predictor.html", form_input = display_form_input, result = prediction_text)


if __name__ == "__main__":
    app.run()
