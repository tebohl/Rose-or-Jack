# Import necessary libraries
from pickle import load
import numpy as np
from flask import Flask, render_template, request

# Flask Setup
app = Flask(__name__)

# Load ML Model
model = load(open('model_randomforrest_2022080848.pkl', 'rb'))
# Load the Scaler
scaler = load(open('scaler.pkl', 'rb'))

# Create routes for each html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visual")
def visual():
    return render_template("visualizations.html")

@app.route("/models")
def models():
    return render_template("models.html")

# Create routes for form entry
@app.route("/form")
def form():

    prediction_text = ""

    return render_template("predictor.html", result = prediction_text)

@app.route("/send", methods=["POST"])
def send():
    # Define variables for one hot coded variables
    firstclass= 0
    secondclass= 0
    thirdclass= 0
    male= 0
    female= 0
    # Obtain form inputs and add to numpy array or dataframe
    name = request.form["survivedname"]
    age = float(request.form["survivedage"])
    fare = float(request.form['survivedfare'])
    converted_fare = fare/154
    family = float(request.form['survivedfamily'])
    pclass = request.form["class"]
    if pclass == "1st":
        firstclass= 1
    elif pclass == "2nd":
        secondclass= 1
    else:
        thirdclass= 1
    sex = request.form["survivedsex"]
    if sex == "Male":
        male= 1
    else:
        female= 1
    # List with feature entries to send to model for prediction
    features= [age, converted_fare, family, firstclass, secondclass, thirdclass, female, male]
   
    # Transform list into numpy array and apply scaler
    final_features = [np.array(features)]
    features_scaled = scaler.transform(final_features)

    # Use form results to make prediction
    prediction = model.predict(features_scaled)[0]

    # Create html content with prediction result
    if prediction == 1: 
        prediction_text = f"Congratulations, {(name)}! You survived!"
    else:
        prediction_text = f"Sorry {(name)}- You did not survive."
    display_form_input = f"You played as a {(int(age))} year old {(sex)}, traveling with {int((family))} family members. You paid ${(int(fare))} to travel in {(pclass)} class."

    # Send prediction to html page
    return render_template("predictor.html", form_input = display_form_input, result = prediction_text)


if __name__ == "__main__":
    app.run()
