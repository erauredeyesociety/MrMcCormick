# Pass entire PDFs through OCR so that the text of the pdf can be easily selected, searched, or extracted 

'''
Some Setup

* Python Packages
    pip install ocrmypdf pytesseract camelot-py Pillow

* Install tesseract-ocr
    https://tesseract-ocr.github.io/tessdoc/Installation.html

* Install ghostscript under AGPL release
    https://ghostscript.com/releases/gsdnld.html

* Check ghostscript bin & lib folders in PATH
    Example - for windows
        C:\Program Files\gs\gs10.00.0\bin
        C:\Program Files\gs\gs10.00.0\lib
'''

import ocrmypdf
import pytesseract
import os
from tqdm import tqdm
from colorama import Fore

pytesseract.pytesseract.tessaract_cmd = pytesseract.pytesseract.tesseract_cmd = (
    "C:\\Program Files\\Tesseract-OCR\tesseract.exe"
)

def ocr(orig_file, new_file):
    ocrmypdf.ocr(orig_file, new_file, skip_text=True) # remove_background=True, rotate_pages=True, deskew=True, 

def check_path(folder_path):
    if os.name == "nt":
        if folder_path[:-1] != "\\":
            folder_path += "\\"
    else:
        if folder_path[:-1] != "/":
            folder_path += "/"
    return folder_path

def main():
    folder_path = input("Example: /opt/tmp/pdfs_dir\nExample: C:\\tmp\\pdfs_dir\n\nEnter The Path to PDFs Folder: ")
    folder_path = check_path(folder_path)

    out_path = os.path.join(folder_path, "ocr_pdfs")
    out_path = check_path(out_path)
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

    for file in tqdm(pdf_files, desc="Processing PDFs"):
        input_file_path = os.path.join(folder_path, file)
        output_file_path = os.path.join(out_path, file)

        if not os.path.exists(output_file_path):
            ocr(input_file_path, output_file_path)
            print(Fore.GREEN + "\n\nDone processing " + Fore.BLUE + f"{file}\n\n" + Fore.RESET)
        else:
            print(Fore.YELLOW + f"\nSkipped {file} as it already exists\n" + Fore.RESET)

if __name__ == "__main__":
    main()
