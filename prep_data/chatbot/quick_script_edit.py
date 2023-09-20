import os
import re

# scan lines in each file
def remove_brackets_n_blanks(file):
    lines = []
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if "[" in line:
                line = re.sub(r"\[.*?\]", "", line)
            if "(" in line:
                line = re.sub(r"(.*?)", "", line)
            lines.append(line)
        for line in lines:
            if not line.strip():
                lines.remove(line)
    return lines

file = "tmp.txt"
new_file = "tmp2.txt"
# scan lines in file
lines = remove_brackets_n_blanks(file)
# write to new file
with open(new_file, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line)

