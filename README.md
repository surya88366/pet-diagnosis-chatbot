# 🐾 Pet Diagnosis Chatbot

An interactive web-based chatbot designed to provide preliminary diagnoses and treatment suggestions for common pet symptoms. This tool helps pet owners quickly identify potential health issues and decide on the next steps.

## ✨ Key Features

- **Interactive Chat Interface:** A simple and user-friendly web interface for easy interaction.
- **Multi-Turn Conversation:** Guides the user by first asking for the pet's name and then the specific symptom.
- **Smart Symptom Matching:** Uses fuzzy string matching to understand user input, even with typos or slight variations.
- **Comprehensive Knowledge Base:** Sources its information from a detailed CSV file, covering a wide range of animals including:
    - Dogs & Cats
    - Birds (Parrots, Finches, etc.)
    - Small Mammals (Rabbits, Hamsters, Guinea Pigs)
    - Reptiles (Snakes, Turtles, Chameleons)
    - Farm Animals (Cows, Goats)
- **Instant Results:** Provides a potential disease and a recommended treatment plan based on the user's input.

## 💻 Technology Stack

- **Backend:** Python
- **Web Framework:** Flask
- **Data Manipulation:** Pandas
- **String Matching:** Python's `difflib` library
- **Frontend:** HTML, CSS, JavaScript (via Fetch API)

## 🚀 How It Works

The application logic follows a simple conversational flow managed by a Flask session:

1.  **Welcome:** The user is greeted and prompted to enter a pet's name.
2.  **Pet Identification:** The backend receives the pet's name, finds the closest match in the dataset, and stores it in the session.
3.  **Symptom Query:** The chatbot asks for the pet's symptom.
4.  **Diagnosis:** The backend filters its dataset for the specific pet and finds the closest matching symptom.
5.  **Response:** The application retrieves the corresponding "Possible Disease" and "Treatment/Solution" and displays it to the user.
6.  **Continue/Stop:** The user is given the option to start a new diagnosis or end the session.

---
*This project is for informational purposes only and does not replace professional veterinary advice. Always consult a licensed veterinarian for any health concerns with your pet.*
