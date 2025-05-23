import json
import random
import re
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Download NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()
stopwords = set(nltk.corpus.stopwords.words('english'))  # Load stopwords

# Load the intents file
file_path = 'health.json'

def load_intents_health(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        intents = json.load(f)
    return intents

# Preprocess the data
def preprocess_data_health(intents):
    questions = []
    tags = []
    for intent in intents['intents']:
        # Check for either 'questions' or 'patterns' key
        if 'questions' in intent:
            for question in intent['questions']:
                questions.append(question)
                tags.append(intent['tag'])
        elif 'patterns' in intent:
            for pattern in intent['patterns']:
                questions.append(pattern)
                tags.append(intent['tag'])
        else:
            print(f"Warning: Missing 'questions' or 'patterns' in intent with tag '{intent.get('tag', 'unknown')}'")
    return questions, tags


# Train the chatbot using Logistic Regression for classification
def train_chatbot_health(intents):
    questions, tags = preprocess_data_health(intents)
    
    # Convert questions to numerical form using TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions)
    
    # Encode the target labels (tags)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(tags)

    # Train a Logistic Regression model
    model = LogisticRegression()
    model.fit(X, y)

    return vectorizer, label_encoder, model

# Get a response based on user input
def get_response_health(user_input, vectorizer, label_encoder, model, intents):
    # Clean and tokenize user input
    user_input = re.sub(r'\W', ' ', user_input.lower())  # Remove punctuation and convert to lower
    user_tokens = nltk.word_tokenize(user_input)  # Tokenize
    user_tokens = [lemmatizer.lemmatize(token) for token in user_tokens if token not in stopwords]  # Lemmatize and remove stopwords
    user_input_processed = ' '.join(user_tokens)

    # Transform the user input using the trained TF-IDF vectorizer
    user_input_vector = vectorizer.transform([user_input_processed])

    # Predict the tag using the trained Logistic Regression model
    predicted_tag_index = model.predict(user_input_vector)[0]
    predicted_tag = label_encoder.inverse_transform([predicted_tag_index])[0]

    # Return the corresponding response
    for intent in intents['intents']:
        if intent['tag'] == predicted_tag:
            return random.choice(intent['responses'])

    return "I'm sorry, I didn't understand that."

# Main function
def main():
    intents = load_intents_health(file_path)
    vectorizer, label_encoder, model = train_chatbot_health(intents)
    
    print("Chatbot is running! Type 'exit' to end the chat.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = get_response_health(user_input, vectorizer, label_encoder, model, intents)
        print("Bot:", response)

if __name__ == "__main__":
    main()
