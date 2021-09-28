import pickle
import argparse
import yaml
import random
from pathlib import Path
from OCR_csv import OCR_and_augment
from twitter_tools import generate_search_url

# tests_path = "D:\\Dokumente\\Uni_OFFLINE\\SS2021\\NLP\\project\\tests\\"

def load_model(model_path):
    """
    loads any trained model from model_path

    args: 
        model_path (path-like): read from config.yaml

    retuns:
        model (sklearn.svm.SVC): trained classifier
    """
    with open(model_path, "rb") as pickle_infile:
        model = pickle.load(pickle_infile)
    return model

def predict(model, OCR_data):
    """
    predicts augmented OCR data based on given model

    args:
        model (sklearn.svm.SVC): trained classifier from load_model
        OCR_data (pd.DataFrame): from OCR_and_augment
    
    returns:
        prediction_dict (dict): includes name, author, text, source
    """
    OCR_data = OCR_data.dropna(subset=["text"])
    prediction = model.predict(OCR_data.iloc[:,11:17].drop(["text"],axis=1))
      
    predicted_name = OCR_data.iloc[prediction == "is_name"]["text"].tolist()
    predicted_authors = OCR_data.iloc[prediction == "is_author"]["text"].tolist()
    predicted_text = OCR_data.iloc[prediction == "is_text"]["text"].tolist()
    predicted_source = OCR_data.iloc[prediction == "is_source"]["text"].tolist()
    
    prediction_dict = {"name" : predicted_name, "author" : predicted_authors, "text" : predicted_text, "source" : predicted_source}  
    return prediction_dict

def get_random_test(tests_path):
    tests = [e for e in Path(tests_path).glob("*.png")]
    sample_path = random.sample(tests,1)[0]
    return sample_path

def print_prediction(prediction_dict):
    """
    prints the contents of prediciton_dict with indentation

    args:
        prediction_dict (dict): from predict()

    returns:
        None
    """
    print("predicted name:\t\t{}".format(prediction_dict["name"]))
    print("predicted authors:\t{}".format(prediction_dict["author"]))
    print("predicted text:\t\t{}".format(prediction_dict["text"]))
    print("predicted source:\t{}".format(prediction_dict["source"]))
    return 

def main():
    trained_model = load_model(model_path)
    ## this is for testing
    # random_test = get_random_test(tests_path)
    # print(random_test)
    # random_OCR = OCR_and_augment(random_test)
    # inference = predict(trained_model,random_OCR)
    parser = argparse.ArgumentParser()
    parser.add_argument("input_img", help="path to an .png image of a tweet screenshot")
    parser.add_argument("-p", "--preds", help="prints prediced name, author, text, source", action="store_true")
    parser.parse_args()
    args = parser.parse_args()
    input_OCR = OCR_and_augment(args.input_img)
    inference = predict(trained_model,input_OCR)
    if args.preds:
        print_prediction(inference)
    # print("inference executed")
    print(generate_search_url(inference["author"],inference["text"]))

if __name__ == "__main__":
    #load some information from config.yaml
    config_path = "config.yaml"
    with open(config_path, "r", encoding="utf8") as config_file:
        config_info = yaml.safe_load(config_file.read())

    model_path = config_info["model_path"]
    tests_path = config_info["tests_path"]
    
    main()

