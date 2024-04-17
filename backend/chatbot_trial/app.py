from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random
import numpy as np
import pickle
import json
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import nltk
from collections import deque
from statistics import mode

# Load NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load trained model and other required data
model = load_model('chatbot_model.h5')
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))
intents = json.loads(open("intents.json").read())
lemmatizer = WordNetLemmatizer()

# Initialize deque to store last 5 emotions
emotion_history = deque(maxlen=5)

# Function to process user message and generate chatbot response
def chatbot_response(msg):
    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(sentence, words, show_details=True):
        sentence_words = clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    def predict_class(sentence, model):
        p = bow(sentence, words, show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(ints, intents_json):
        tag = ints[0]["intent"]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
        return result

    # Process message and get chatbot response
    ints = predict_class(msg, model)
    res = get_response(ints, intents)
    print(res)
    return res

# Endpoint to receive messages from React frontend
@app.route("/chatbot", methods=["POST"])
@cross_origin()  # Enable CORS for this route
def handle_message():
    try:
        data = request.get_json()
        message = data["message"]

        # If the message starts with "Emotion: ", treat it as emotion data
        if message.startswith("Emotion: "):
            # Extract the emotion from the message
            emotion = message.replace("Emotion: ", "")
            print("Detected Emotion:", emotion)
            
            # Store the emotion in history
            emotion_history.append(emotion)
            
            # Get the mode of last 5 emotions
            if len(emotion_history) == 5:
                mode_emotion = mode(emotion_history)
                print("Mode of last 5 emotions:", mode_emotion)
                response = f"Mode of last 5 emotions: {mode_emotion}"
            else:
                response = "Not enough emotions for calculation."
        else:
            # Process the user's message as usual
            response = chatbot_response(message)

        return jsonify({"response": response})
    except Exception as e:
        print("Error fetching response: ", str(e))
        return jsonify({'response': "Sorry, didn't get you"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
