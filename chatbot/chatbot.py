import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from data_handling import *
import json
import numpy as np

def check_in_dir(in_dir):
    if not os.path.exists(in_dir):
        os.makedirs(in_dir)
    if os.name == "nt":
        if in_dir[:-1] != "\\":
            in_dir += "\\"
    else:
        if in_dir[:-1] != "/":
            in_dir += "/"
    return in_dir

# Load Model Files from a specific directory
in_dir = "chatbot_model_files"
in_dir = check_in_dir(in_dir)

# the maximum number of words in the vocabulary
num_words_vocab = 20000
max_sequence_length = 20


# Load the trained model and its weights
model = load_model(os.path.join(in_dir + "model.h5"))
model.load_weights(os.path.join(in_dir + "weights.h5"))

# Load the tokenizer from tokenizer.json
with open(os.path.join(in_dir + "tokenizer.json")) as f:
    data = json.load(f)
    tokenizer = Tokenizer(num_words=num_words_vocab)
    tokenizer.word_index = data

# Create a function to encode the input text
def encode_text(text):
    text = text.lower()
    text = text.split()
    text = [tokenizer.word_index[word] for word in text if word in tokenizer.word_index]
    text = pad_sequences([text], maxlen=max_sequence_length, padding='post')
    return text

# Create a function to generate a response
def generate_response(input_text):
    encoded_text = encode_text(input_text)
    prediction = model.predict(encoded_text)
    response = np.argmax(prediction[0])
    if response >= num_words_vocab:
        decoded_response = "I don't know what to say."
    else:
        decoded_response = tokenizer.index_word[response]
    return decoded_response


# Create a loop to take user input and print responses
while True:
    input_text = input("You: ")
    if input_text.lower() == "exit":
        break
    response = generate_response(input_text)
    print("Chatbot: ", response)
