from PIL import Image
from pathlib import Path
import pytesseract
import numpy as np
import pandas as pd
import matplotlib as plt
import re
import yaml

#test img load.
test_img = Image.open("D:\\Dokumente\\Uni_OFFLINE\\SS2021\\NLP\\project\\tweets\\test2.png")
test_path = "D:\\Dokumente\\Uni_OFFLINE\\SS2021\\NLP\\project\\tweetcaptures\\1433049065609121794.png"

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

# OCR_data = pytesseract.image_to_data(test_img,output_type="data.frame")

# print(OCR_data)
# print(type(out))

#add relative width and height data for every entry
def OCR_and_augment(input_img):
    """
    runs OCR on input image and augments the dataframe it then outputs.
    """
    #OCR
    img = Image.open(input_img)
    data = pytesseract.image_to_data(img,output_type="data.frame")
    #augmentation
    data["rel_left"] = data["left"] / img.width
    data["rel_top"] = data["top"] / img.height
    data["rel_center_x"] = (data["left"] + (data["width"]/ 2))  / img.width
    data["rel_center_y"] = (data["top"] + (data["height"]/ 2))  / img.height
    data["is_handle"] = data["text"].str.match("@(\w){3,15}$",na=False).astype(int)
    return data

def save_OCR(input_data,path): #not really useful right now.
    input_data.to_csv(path,index=False)
    return

def load_OCR(filepath):
    if Path(filepath).exists():
        OCR_data = pd.read_csv(filepath)
    else: 
        # save_OCR(OCR_and_augment(filepath.rstrip(".csv") + ".png"),filepath.rstrip(filepath.stem() + ".csv")) #issue in this line
        # print(filepath.parent)
        save_OCR(OCR_and_augment(Path(str(filepath.parent) + "\\" + str(filepath.stem) + ".png")), filepath)
        OCR_data = pd.read_csv(filepath)
    return OCR_data

# print(OCR_data)
# print(OCR_and_augment(img).head(50))

#find author (by matching "@.+")
# print(out["text"][out["text"].str.match("@.+") == True])

def get_handles(in_data): #unused.
    """
    returns a list of twitter handles

    Parameters
    ----------
    in_data : data.frame
        data.frame returned from OCR_and_augment()
    
    Returns
    -------
    list
        twitter @handle strings
    """
    return [row["text"] for row in in_data.iloc if row["is_handle"] == 1] 
# print(get_author(OCR_data))

def get_text(in_data): #not working
    """
    returns the text as string

    Parameters
    ----------
    in_data : data.frame
        data.frame returned from pytesseract.image_to_data()
    
    Returns
    -------
    str
        tweet content
    """
    #line_num between 0 and 0 
    #par_num == 2
    output = ""
    for row in in_data.iloc:
        if (row["par_num"] == 2) and (row["line_num"] > 1):            
            if type(row["text"]) == str:
                output += row["text"] + " "
    return output
    
# print(get_text(OCR_and_augment(img)))

# print(pytesseract.image_to_boxes(img))

# print(OCR_and_augment(test_path))