from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from markupsafe import Markup
import pandas as pd
import difflib

# Load the dataset
file_path = 'Final_Datasets.csv'  # Update this path as necessary
pet_dataset = pd.read_csv(file_path)

app = Flask(__name__)
app.secret_key = 'secret_key_for_session_management'  # Replace with a secure key in production

# Function to get the closest match for the user input
def get_closest_match(user_input, valid_values):
    matches = difflib.get_close_matches(user_input.lower(), valid_values, n=1, cutoff=0.6)
    return matches[0] if matches else None

@app.route("/", methods=["GET"])
def home():
    # Render the index page
    session.clear()  # Clear session on home page
    return render_template("index.html")

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/login", methods=["GET"])
def login():
    # Render the login page
    return render_template("login.html")

@app.route("/chatbot", methods=["GET"])
def chatbot():
    # Render the chatbot page
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("user_message", "").strip().lower()

    # Check if the user wants to continue
    if "continue" in session and session["continue"]:
        if user_message == "continue":
            session.clear()  # Clear session to restart
            return jsonify({"bot_response": "Please enter the pet's name (e.g., 'dog', 'cat')."})
        elif user_message == "stop":
            session.clear()  # Clear session and end
            return jsonify({"bot_response": "Thank you for using the Pet Diagnosis Chatbot. Goodbye!"})

    # If pet name hasn't been provided yet, ask for it first
    if "pet_name" not in session:
        pet_names = pet_dataset['Pet Name'].str.lower().unique()
        closest_pet_name = get_closest_match(user_message, pet_names)

        if closest_pet_name:
            session["pet_name"] = closest_pet_name  # Save the pet name in the session
            return jsonify({"bot_response": f"Thank you! Now please enter the symptom for {closest_pet_name.capitalize()}."})
        else:
            return jsonify({"bot_response": f"Invalid pet name '{user_message}'. Please enter a valid pet name."})

    # If pet name is in session but symptom hasn't been provided yet, ask for it
    elif "symptom" not in session:
        pet_name = session["pet_name"]
        pet_symptoms = pet_dataset[pet_dataset['Pet Name'].str.lower() == pet_name]['Symptom'].str.lower().unique()
        closest_symptom = get_closest_match(user_message, pet_symptoms)

        if closest_symptom:
            # Filter the dataset for the selected pet and symptom
            result = pet_dataset[(pet_dataset['Pet Name'].str.lower() == pet_name) &
                                (pet_dataset['Symptom'].str.lower() == closest_symptom)]
            if not result.empty:
                disease = result['Possible Disease'].values[0]
                treatment = result['Treatment/Solution'].values[0]
                # Clear session after response and ask to continue
                session["continue"] = True  # Set continue session variable
                response = Markup(f"Possible Disease: {disease}<br><br>Recommended Treatment: {treatment}<br><br>Do you want to continue? Type 'continue' to proceed or 'stop' to exit.")
                return jsonify({"bot_response": response})
            else:
                return jsonify({"bot_response": f"No information found for {closest_symptom} in {pet_name.capitalize()}."})
        else:
            return jsonify({"bot_response": f"No matching symptom found for '{user_message}' in {pet_name.capitalize()}. Please try another symptom."})

    # Reset and ask for both pet name and symptom if the flow is broken
    session.clear()
    return jsonify({"bot_response": "Please enter the pet name first."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
