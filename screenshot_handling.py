from typing import Annotated
from tweetcapture import TweetCapture
import pandas as pd
import asyncio
import json
import yaml
from pathlib import Path
from twitter_tools import get_tweet_link, sample_stream_ids, tweet_lookup, load_lookup,save_lookup
from OCR_csv import OCR_and_augment,save_OCR,load_OCR



def generate_screenshots(tweet_ids,path):
    """
    generates tweet screenshots
    
    Params:
        tweet_ids (list): list of int tweet_ids
        path (str): directory where to save screensshots at.

    Returns: 
        nothing?
    """
    # print(tweet_ids)
    for tweet_id in tweet_ids:
        asyncio.run(tweet.screenshot(get_tweet_link(tweet_id), path + str(tweet_id) + ".png", mode=3, night_mode=1)) #lang=en?
        # print("tweet_id {} screenshot generated".format(tweet_id))
    return 

def print_info(directory):
    """
    prints and saves all OCR and lookup data for all screenshots in the directory
    """
    for screenshot in Path(directory).glob("*.png"):
        print(str(screenshot))
        print(OCR_and_augment(screenshot))
        save_OCR(OCR_and_augment(screenshot),directory + screenshot.stem + ".csv")
        print(json.dumps(tweet_lookup(screenshot.stem), indent=2, sort_keys=True))
        with open(directory + screenshot.stem + ".json", "w", encoding = "utf8") as json_outfile:
            json.dump(tweet_lookup(screenshot.stem), json_outfile)
        print(get_tweet_link(screenshot.stem))        
        print("---------")      
        # break # so I can just look at a single tweet...
    return 

def generate_tests(amount):
    tests_path = "D:\\Dokumente\\Uni_OFFLINE\\SS2021\\NLP\\project\\tests\\"
    generate_screenshots(sample_stream_ids(amount),tests_path)

def annotate_tweet(OCR_data,lookup_data):
    """
    takes OCR_data and lookup_data from a tweet screenshots and annotates new rows.
    """

    # annotated_OCR = OCR_data.copy()
    #annotated is_name?
    OCR_data["is_name"] = OCR_data["text"].dropna().isin(lookup_data["includes"]["users"][0]["name"].split()).astype(int) # this annotates is_name?
        
    #annotate is_author
    OCR_data["is_author"] = (OCR_data["text"].str.lstrip("@") == lookup_data["includes"]["users"][0]["username"]).astype(int) # this annotates is_author...
        
    #annotate is_text
    OCR_data["is_text"] = OCR_data["text"].dropna().isin(lookup_data["data"][0]["text"].split()).astype(int) #this annotates is_text to some degree, might need a pop or a cleanup from start to end.
    
    #annotated is_time?

    #annotated is_source
    OCR_data["is_source"] = OCR_data["text"].dropna().isin(lookup_data["data"][0]["source"].split()).astype(int) #this annotates is_text to some degree, might need a pop or a cleanup from start to end.
    
    #cleanup?


    return OCR_data


def main():
    # generate_screenshots(sample_stream_ids(25),captures_path)
    
    # loop all .png tweet screenshots
    for screenshot in Path(captures_path).glob("*.png"):
        tweet_id_path = captures_path + screenshot.stem
        OCR_data = load_OCR(Path(tweet_id_path + ".csv"))
        lookup_data = load_lookup(Path(tweet_id_path + ".json"))
        annotate_tweet(OCR_data,lookup_data)

        save_OCR(OCR_data, captures_path + screenshot.stem + ".csv")
        save_lookup(lookup_data, captures_path + screenshot.stem + ".json")

    #loop on all .json tweet looups
    # for lookup in Path(captures_path).glob("*.json"):1
    #     print(json.dumps(load_lookup(lookup), indent=2, sort_keys=True))
    
    #loop on all .csv OCR datas
    # for OCR in Path(captures_path).glob("*.csv"):
        # save_OCR(OCR_and_augment(OCR))
        #   print(load_OCR(OCR))
    
    # generate_tests(5)

    print("main executed")


if __name__ == "__main__":
    #load some information from config.yaml
    config_path = "project\config.yaml"
    with open(config_path, "r", encoding="utf8") as config_file:
        config_info = yaml.safe_load(config_file.read())

    captures_path = config_info["captures_path"]
    lang = config_info["lang"]

    #init TweetCapture module    
    tweet = TweetCapture()
    tweet.lang = lang

    main()
