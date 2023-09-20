# A recurrent neural network (RNN) that uses movie scripts as a base for a chatbot.

import tensorflow as tf
import numpy as np
from data_handling import *
from sklearn.model_selection import train_test_split
from tensorflow import keras
import keras.backend as K
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.losses import SparseCategoricalCrossentropy
import matplotlib.pyplot as plt

def check_out_dir(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        i = 1
        while not os.path.exists(out_dir+str(i)):
            os.makedirs(out_dir+str(i))
            if os.path.exists(out_dir+str(i)):
                out_dir = out_dir+str(i)
                break
            i += 1
    if os.name == "nt":
        if out_dir[:-1] != "\\":
            out_dir += "\\"
    else:
        if out_dir[:-1] != "/":
            out_dir += "/"
    return out_dir

# Save Model Files to a specific Directory
out_dir = "chatbot_model_files"
out_dir = check_out_dir(out_dir)

# Define the model's architecture
hidden_size = 256
num_time_steps = 100
input_dim = 200
output_dim = 100
max_sequence_length = 20 # respond in 20 words or less

# other hyperparameters
learning_rate = 0.001
batch_size = 32
epochs = 500

data_to_use = 0.2 # use 20% of the data
data_dir_prepped = "./data/chatbot/prepped/" # where the data is stored
num_words_vocab = 20000 # the maximum number of words in the vocabulary
quotes = load_quotes(data_dir_prepped) # Load the quotes from the prepped data directory
prompts, responses = preprocess_quotes(quotes) # Preprocess the quotes
embedding_size = 150 # keep between 100 and 300

# Create a vocabulary of the most common words in the quotes
tokenizer = Tokenizer(num_words=num_words_vocab)
tokenizer.fit_on_texts(prompts)
tokenizer.fit_on_texts(responses)

# Convert the prompts and responses to sequences of integers
prompts_sequences = tokenizer.texts_to_sequences(prompts)
responses_sequences = tokenizer.texts_to_sequences(responses)

# Pad the sequences to the same length
prompts_sequences = keras.preprocessing.sequence.pad_sequences(prompts_sequences, maxlen=max_sequence_length, padding="post")
responses_sequences = keras.preprocessing.sequence.pad_sequences(responses_sequences, maxlen=max_sequence_length, padding="post")
# Create the model
model = keras.models.Sequential([
    keras.layers.Embedding(input_dim=num_words_vocab, output_dim=embedding_size, input_length=max_sequence_length),
    keras.layers.LSTM(hidden_size, return_sequences=True),
    keras.layers.LSTM(hidden_size, return_sequences=True),
    keras.layers.Dense(num_words_vocab, activation="softmax")
])
# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Split the data into training and testing sets
train_prompts, test_prompts, train_responses, test_responses = train_test_split(prompts_sequences, responses_sequences, test_size=0.2)

# Define a ModelCheckpoint callback to save the model's weights during training
checkpoint_path = os.path.join(out_dir, "model.ckpt")
checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True)
# Define a ProgbarLogger callback to print progress to the screen
progbar_callback = keras.callbacks.ProgbarLogger(count_mode="steps")

# Train the model
history = model.fit(train_prompts, train_responses, batch_size=batch_size, epochs=epochs, callbacks=[checkpoint_callback, progbar_callback], verbose=True)

# Evaluate the model on the test data
test_results = model.evaluate(test_prompts, test_responses, batch_size=batch_size, verbose=True)
# Print the test loss and accuracy
test_loss, test_accuracy = test_results
print("Test loss:", test_loss)
print("Test accuracy:", test_accuracy)

# Plot the training accuracy and loss
plt.plot(history.history['accuracy'])
plt.plot(history.history['loss'])
plt.title('Model accuracy and loss')
plt.ylabel('Accuracy/Loss')
plt.xlabel('Epoch')
plt.legend(['Accuracy', 'Loss'], loc='upper left')
plt.show()
# save plt to image in the model files directory
plt.savefig(os.path.join(out_dir, "model_accuracy_and_loss.png"), dpi='figure', transparent=True)

# Save the model's weights
# if the file already exists, make a new file with an integer inserted before the period
# if the new file already exists, increment the integer and try again

if not os.path.exists(os.path.join(out_dir, "weights.h5")):
    model.save(os.path.join(out_dir, "weights.h5"))
else:
    i = 1
    while not os.path.exists(os.path.join(out_dir, "weights" + str(i) + ".h5")):
        i += 1
    model.save(os.path.join(out_dir, "weights" + str(i) + ".h5"))

# Save the tokenizer to a file
# if the file already exists, make a new file with an integer inserted before the period
# if the new file already exists, increment the integer and try again
if not os.path.exists(os.path.join(out_dir, "tokenizer.json")):
    with open(os.path.join(out_dir, "tokenizer.json"), "w") as f:
        f.write(tokenizer.to_json())
else:
    i = 1
    while not os.path.exists(os.path.join(out_dir, "tokenizer" + str(i) + ".json")):
        i += 1
    with open(os.path.join(out_dir, "tokenizer" + str(i) + ".json"), "w") as f:
        f.write(tokenizer.to_json())

# Save the model's architecture to a file
# if the file already exists, make a new file with an integer inserted before the period
# if the new file already exists, increment the integer and try again

if not os.path.exists(os.path.join(out_dir, "model.h5")):
    model.save(os.path.join(out_dir, "model.h5"))
else:
    i = 1
    while not os.path.exists(os.path.join(out_dir, "model" + str(i) + ".h5")):
        i += 1
    model.save(os.path.join(out_dir, "model" + str(i) + ".h5"))
