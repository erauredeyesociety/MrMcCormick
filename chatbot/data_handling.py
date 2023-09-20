import os
import string
from tqdm import tqdm

# each file is part of a script from a movie
# each line is a line of dialogue
# each line is either a sequence or a response
# the sequence lines are spoken to the chatbot
# the response lines are spoken by the chatbot

'''
Example Formatting:
S: How are you doing today
R: I am fine
S: What is your favorite color
R: Blue
S: What is your favorite animal
R: Dogs
S: This should be interesting
R: Your not my type
S: Smart?
R: Single
'''

# you can change what the sequence lines and response lines start with.
sequence_line_starter = "S: "
response_line_starter = "R: "

# example - ./data/chatbot/tmp
data_dir_train = "./data/chatbot/tmp"

def load_quotes(data_dir):
    """Load quotes from text files in the given data directory.

    Args:
        data_dir: The directory where the text files are located.

    Returns:
        A list of quotes, where each quote is a string.
    """
    data = []
    for file_name in tqdm(os.listdir(data_dir), desc="Load Data From Files"):
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r", encoding='utf-8') as f:
            for line in f:
                # Extract the quote from the line
                for line in f:
                    data.append(line.strip())
    return data

def preprocess_quotes(data):
    """Preprocess the data by splitting it into sequences and responses.

    Args:
        data: A list of strings where each string is a line of text.

    Returns:
        A tuple (sequences, responses) where sequences is a list of sequences
        and responses is a list of responses.
    """
    prompts = []
    responses = []
    for i in tqdm(range(len(data)), desc="Process Quotes In Files"):
        line = data[i]
        # separate sequence vs response lines
        # if a line does not start with the sequence_line_starter, or the response_line_starter, it is ignored
        if line.startswith(sequence_line_starter):
            prompts.append(line[len(sequence_line_starter):])
            #print("Prompt: " + line[len(sequence_line_starter):])
        elif line.startswith(response_line_starter):
            responses.append(line[len(response_line_starter):])
            #print("Response: " + line[len(sequence_line_starter):])
        else:
            print("Unable to store: \n "+line)
    
    return prompts, responses


def test():
    data = load_quotes(data_dir_train)
    prompts, responses = preprocess_quotes(data)
    print("Number of sequences:", len(prompts))
    print("Number of responses:", len(responses))

    # save the sequences and responses to files
    with open("sequences.txt", "w", encoding="utf-8") as f:
        for sequence in tqdm(prompts, desc="Loading Prompts"):
            f.write(sequence + "\n")

    with open("responses.txt", "w", encoding="utf-8") as f:
        for response in tqdm(responses, desc="Loading Responses"):
            f.write(response + "\n")

    print("Done")