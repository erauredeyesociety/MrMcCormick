# organize the movies scripts
import os

def remove_whitespace(new_file):
    # remove brackets and blank lines
    lines = []
    with open(new_file, "r", encoding="utf-8") as f:
        for line in f:
            if "[" in line:
                line = re.sub(r"\[.*?\]", "", line)
            lines.append(line)
        for line in lines:
            if not line.strip():
                lines.remove(line)
    # write the lines to a new file
    with open(new_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)

def remove_non_speech(new_file):
    # remove lines that are not speech
    # speech lines contain colons after the first word
    # if there is not a colon before the first space in the line, then remove the line

    with open(new_file, 'rw') as f:
        lines = f.readlines()
        for line in lines:
            # if line contains a colon before the first space, then it is a speech line
            if ":" in line[:line.index(" ")]:
                continue
            # if line does not contain a colon before the first space, then it is not a speech line
            else:
                lines.remove(line)
        # write the lines to a new file
        for line in lines:
            f.write(line)

def remove_chars(orig_file, new_file):
    chars_2_remove = ['*', '?', '|', '(', ')', '{', '}', '[', ']', '.', '^']
    with open(orig_file, 'r') as f:
        lines = f.readlines()
        # remove characters from lines
        for line in lines:
            for character in chars_2_remove:
                new_line = line.replace(character, '')
            lines[lines.index(line)] = new_line
        # write the lines to a new file
        with open(new_file, 'w') as f:
            f.writelines(lines)

def main():

    # get directory of current file
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    # go up one directory from current directory
    up_dir = os.path.dirname(curr_dir)
    # raw data dir is located in the data dir
    orig_data = up_dir + "/data/raw/"
    new_data_dir = up_dir + "/data/prepped/"


    # check if new data dir exists
    if not os.path.exists(new_data_dir):
        os.makedirs(new_data_dir)
    else:
        # if new data dir already exists, make a directory with an integer appended to the name
        i = 0
        while os.path.exists(new_data_dir + str(i)):
            i += 1
        new_data_dir = new_data_dir + str(i)
        os.makedirs(new_data_dir)

    print("New Directory: " + new_data_dir)

    # for file in orig data, process lines and write to new files
    for file in os.listdir(orig_data):
        # if file is a txt file
        if file.endswith(".txt"):
            orig_file = os.path.join(orig_data, file)
            new_file = os.path.join(new_data_dir, file)
            print("Removing characters from " + file + "...")
            remove_chars(orig_file, new_file)
            print("Removing whitespace from " + file + "...")
            remove_whitespace(new_file)
            print("Removing non-speech from " + file + "...")
            remove_non_speech(new_file)
main()