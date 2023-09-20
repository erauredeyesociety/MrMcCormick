# Outputs pdf text to text files.
# Then sorts the text files into one "sentence" per line
# useful for turning pdfs into audiobooks, or dialouges

import shutil
import traceback
import PyPDF2
from colorama import Fore
import os
from tqdm import tqdm

# use this tool to convert text to mp3
# https://audio.online-convert.com/convert/txt-to-mp3

txt_out_dir = "pdf_sentences"

file_names = []

prog_str = Fore.GREEN + "[+] " + Fore.RESET
neg_str = Fore.RED + "[-] " + Fore.RESET

replace_with_space = [
    "\t",
    ",\n",
    "(\n",
    ")\n",
    "[\n",
    "]\n",
    "{\n",
    "}\n",
    '"\n',
    "'\n",
    ":\n",
    ";\n",

    # the alphabet
    "A\n",
    "B\n",
    "C\n",
    "D\n",
    "E\n",
    "F\n",
    "G\n",
    "H\n",
    "I\n",
    "J\n",
    "K\n",
    "L\n",
    "M\n",
    "N\n",
    "O\n",
    "P\n",
    "Q\n",
    "R\n",
    "S\n",
    "T\n",
    "U\n",
    "V\n",
    "W\n",
    "X\n",
    "Y\n",
    "Z\n",

    "a\n",
    "b\n",
    "c\n",
    "d\n",
    "e\n",
    "f\n",
    "g\n",
    "h\n",
    "i\n",
    "j\n",
    "k\n",
    "l\n",
    "m\n",
    "n\n",
    "o\n",
    "p\n",
    "q\n",
    "r\n",
    "s\n",
    "t\n",
    "u\n",
    "v\n",
    "w\n",
    "x\n",
    "y\n",
    "z\n",

    # numbers
    "0\n",
    "1\n",
    "2\n",
    "3\n",
    "4\n",
    "5\n",
    "6\n",
    "7\n",
    "8\n",
    "9\n",
]

replace_with_newline = [ 
    "\n",
    "\n\t",
]

punctuation_2_newline = [".", "!", "?"]

super_specific_edits = {
    ".\n.\n.\n": ", ",
    ".\n.\n.\n": ", ",
    " ." : ".",
    "\n\"" : "\"",
    "!\n?" : "!?",
    "?\n!" : "?!",
    "!\n!" : "!!",
    ".\"" : ".\"",
    "?\"" : "?\"",
    "!\"" : "!\"",
    "!\n\"" : "!\"",
    "?\n\"" : "?\"",
    ".\n'" : ".'",
    "?\n'" : "?'",
    "!\n'" : "!'",
    "\n''" : "''",
    "\n”" : "”",
    "\n“" : "“",
    "\n’" : "’",
    "\n‘" : "‘",

    ",  " : ", ",
    ":  " : ": ",
    ";  " : "; ",
    " ," : ",",
    " :" : ":",
    " ;" : ";",

    "\n.com": ".com\n",
    "\n.net": ".net\n",
    "\n.org": ".org\n",
    "\n.gov": ".gov\n",
    "\n.edu": ".edu\n",
    "\n.info": ".info\n",
    "\n.biz": ".biz\n",

    "\n.COM": ".COM\n",
    "\n.NET": ".NET\n",
    "\n.ORG": ".ORG\n",
    "\n.GOV": ".GOV\n",
    "\n.EDU": ".EDU\n",
    "\n.INFO": ".INFO\n",
    "\n.BIZ": ".BIZ\n",
}

class To_Sentences:

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def check_dir_path(self, dir_path):
        if os.name == "nt":
            if dir_path[:-2] != "\\":
                dir_path += "\\"
        else:
            if dir_path[:-1] != "/":
                dir_path += "/"
        return dir_path

    def pdf_to_sentences(self, infile, outfile, file_num, num_files):

        print(prog_str + Fore.CYAN + infile + Fore.RED)

        pdffileobj=open(infile,'rb')
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        x=pdfreader.numPages

        with open(outfile, "w") as f:
            for page in range(x):
                pageobj=pdfreader.getPage(page)
                text=pageobj.extractText()
                
                # if lines don't end with a period, put line on previous line
                text = text.replace("\n", " ")

                for r in replace_with_space:
                    text = text.replace(r, " ")

                for r in replace_with_newline:
                    text = text.replace(r, "\n")
                
                newtext = ""
                # if line does not end in punctuation remove newline at beginning of line
                for line in text.split("\n"):
                    for p in punctuation_2_newline:
                        if not line.endswith(p):
                            line = line.replace("\n", "")
                    newtext += line
                
                # start new line after period or other punctuation
                for p in punctuation_2_newline:
                    newtext = newtext.replace(p, p + "\n")

                for k, v in super_specific_edits.items():
                    newtext = newtext.replace(k, v)

                f.write(newtext)
            f.close()
            print(Fore.GREEN)

    def run_file(self, file_path):
            file_name = file_path.split("/")[-1].split(".")[0] + ".pdf"

            dir_path = file_path.split(file_name)[0]

            out_dir = dir_path + txt_out_dir

            if not os.path.exists(out_dir):
                os.mkdir(out_dir)

            outfile = out_dir + "/" + file_name.split(".")[0] + ".txt"

            
            if not os.path.exists(file_name):
                self.pdf_to_sentences(file_path, outfile, 1, 1)
            else:
                print(prog_str + "Text file already exists for " + Fore.RESET + outfile + ".pdf")

    def run_dir(self, dir_path):
        self.clear_screen()
        dir_path = self.check_dir_path(dir_path)
        out_dir = os.path.join(dir_path, txt_out_dir)
        out_dir = self.check_dir_path(dir_path)
        
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        
        
        num_files = 0
        for file in os.listdir(dir_path):
            if file.endswith(".pdf"):
                file_names.append(file)
                num_files += 1

        curr_file = 1


        print("\n" + Fore.GREEN)
        for file in tqdm(range(num_files), desc="Converting PDFs to text files"):
            print("\n")
            try:
                file = file_names[file]
                file_name = file.split(".")[0]
                outfile = os.path.join(out_dir, (file_name + ".txt"))
                if not os.path.exists(outfile):
                    self.pdf_to_sentences(dir_path + file, outfile, curr_file, num_files)
                    #shutil.move(file_name + ".txt", out_dir)
                else:
                    print(prog_str + "Text file already exists for " + Fore.RESET + file_name + ".pdf" + "\n")
                curr_file += 1
            except:
                print(neg_str + Fore.RED + "Error converting " + Fore.RESET + file_name + ".pdf")
                # print the error
                print(traceback.format_exc())
                print("\n")
                curr_file += 1
                continue

def main():
    print("Would you like to convert a single file or a directory?")
    print("1. Single file")
    print("2. Directory")
    print("3. Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        file_path = input("Enter file path: ")
        To_Sentences().run_file(file_path)
    elif choice == "2":
        dir_path = input("Enter directory path: ")
        To_Sentences().run_dir(dir_path)
    elif choice == "3":
        exit()
    else:
        print(neg_str + Fore.RED + "Invalid choice" + Fore.RESET)
        main()

if __name__ == "__main__":
    main()