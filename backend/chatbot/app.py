from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import random
import json
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import torch
from transformers import BertTokenizer, pipeline
import requests
from collections import deque
from statistics import mode

# Load intents JSON file
#SHAUN's

app = Flask(__name__)
CORS(app)

with open('intents.json') as file:
    intents = json.load(file)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
nltk.download('punkt')
nltk.download('wordnet')
vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
lemmatizer = WordNetLemmatizer()
model = torch.load('complete_bert_model.pth', map_location=torch.device('cpu'))
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
globalEmotion="default"
# Set the model to evaluation mode
model.eval()
# Implement other necessary functions here
label_encoder=LabelEncoder()


#@app.route('/predict_intent', methods=['POST'])
# def predict_intent():
#     content = request.json
#     user_input = content['user_input']
#     text=user_input
#     tokenized_text = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
#     input_ids = tokenized_text['input_ids'].to(device)
#     attention_mask = tokenized_text['attention_mask'].to(device)

#     # Make predictions
#     with torch.no_grad():
#         outputs = model(input_ids, attention_mask=attention_mask)
#         logits = outputs.logits
#         predictions = torch.argmax(logits, dim=1)
#         predicted_label = label_encoder.inverse_transform(predictions.cpu().numpy())[0]

#     # Implement the logic to predict intent here
#     # Return the predicted intent as a JSON response
#     return jsonify({"intent": predicted_label})

@app.route('/get_news', methods=['GET'])
def get_news_route():
    api_key = "pub_42178cd805bab2a380ec6db75438d5afc14b7"  # Replace 'YOUR_API_KEY' with your actual API key
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=latest"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "success":
        articles = data.get("results")
        news_list = []
        for article in articles:
            title = article.get("title")
            description = article.get("description")
            news_list.append({"title": title, "description": description})
        return jsonify({"news": news_list})
    else:
        return jsonify({"error": "Error fetching news data. Check your API key or try again later."}), 500
@app.route('/updateEmo', methods=['POST'])
def updation():
    global globalEmotion
    input = request.get_json()
    emotion = input["message"]
    if emotion == "Happy":
        globalEmotion = "joy"
    elif emotion == "Sad":
        globalEmotion = "sadness"
    elif emotion == "Fear":
        globalEmotion = "fear"
    elif emotion == "Surprise":
        globalEmotion = "joy"
    return jsonify({"updated": "hi"})
@app.route('/chatbot', methods=['POST'])
@cross_origin()
def chat():
    try:
        data = request.get_json()
        user_input = data["message"]
        if not user_input:
            return jsonify({"error": "User input is required"}), 400
        
        appreciation_triggers = ['thanks', 'thank you', 'awesome', 'great', 'amazing', 'super', 'cool', 'fantastic', 'good choice', 'nice']
        appreciation_responses = [
            "You're welcome!",
            "No problem, happy to help!",
            "Glad I could assist you!",
            "Anytime!",
            "Don't mention it!",
            "My pleasure!",
            "I'm here to help!",
        ]

        response = None
        last_prompt=None
        labels = []
        patterns = []
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                labels.append(intent['tag'])

        # Use LabelEncoder to convert labels to integers
        label_encoder = LabelEncoder()
        label_encoder.fit(labels)
        encoded_labels = label_encoder.transform(labels)
        if last_prompt is not None and any(trigger in user_input.lower() for trigger in appreciation_triggers):
            response = random.choice(appreciation_responses)
            last_prompt = None

        if response is None:
            if 'name' in user_input.lower():
                response = "It's nice to meet you!"
            else:
                emotion_result = emotion_model(user_input)[0]
                emotion = emotion_result['label']
                if(globalEmotion!="default"):
                    emotion=globalEmotion
                    print("Global:",globalEmotion)
                print("Emotion:",emotion)
                inputs = tokenizer.encode_plus(user_input, add_special_tokens=True, return_tensors="pt")
                inputs = inputs.to(device)
                intent_probabilities = model(**inputs)[0]
                intent_index = intent_probabilities.argmax().item()
                intent_tag = label_encoder.inverse_transform([intent_index])[0]
                for intent in intents['intents']:
                    if intent['tag'] == intent_tag:
                        if intent['tag'] == intent_tag:
                            if emotion in intent['responses']:
                                responses = intent['responses'][emotion]
                            else:
                                responses = intent['responses']['default']
                            response = random.choice(responses)

                        # Check if the intent is "news" and append news headlines to the response
                        if intent['tag'] == 'news':
                            # Get current headlines
                            news_headlines = get_news(api_key)
                            if news_headlines is not None:
                                # Limit the number of headlines to 5
                                news_headlines = news_headlines[:5]
                                # Append news headlines to the response
                                response += "\n\nHere are some of the top headlines:\n"
                                for headline in news_headlines:
                                    if headline['description'] is not None:  # Check if description is not None
                                        response += f"- {headline['title']}\n{headline['description']}\n"
                                break
                            else:
                                response += "\n\nSorry, I couldn't retrieve the news headlines at the moment."
                        break
                else:
                    response = "I'm sorry, I don't understand that."

        return jsonify({"response": response})
    except Exception as e:
        print("Error fetching response: ", str(e))
        return jsonify({'response': "Sorry, didn't get you"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
