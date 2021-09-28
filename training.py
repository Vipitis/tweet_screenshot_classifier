import pickle
import yaml
import pandas as pd
from pytesseract.pytesseract import save
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score,recall_score,precision_score
from pathlib import Path
from OCR_csv import load_OCR

def preprocess(captures_path,test_size=0.2):
    frames = [ load_OCR(frame).dropna(subset=["text"]) for frame in Path(captures_path).glob("*.csv") ] #concat all the frames but ignore rows where text= NaN ...?
    all_OCR = pd.concat(frames).reset_index(drop=True)
    # all_OCR["conf"] = all_OCR["conf"]/100 #normalize conf to 0..1 instead of 0..100
    # all_OCR = all_OCR.drop(all_OCR[all_OCR[["is_name","is_author","is_text","is_source"]].sum(axis=1) == 0].index) #ignore rows without any labels?
    X_data = all_OCR.iloc[:,:17].drop(["text"],axis=1).iloc[:,-5:]
    Y_data = all_OCR.iloc[:,17:].astype(int) #is_author, is_text, is_source -> one hot encoding with cold rows?
    
    # shrink one hot encoding down to a 1d array ?
    Y_data["cat"] = Y_data.loc[Y_data.sum(axis=1) > 0].idxmax(axis=1)
    Y_data = Y_data.fillna("no_data") #might not be the best approach

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=test_size, random_state=41,shuffle=False) #not really needed - and shuffle = flase is questionable
    print(len(X_data))
    return X_train, X_test, y_train, y_test

def train(X,Y):
    clf = svm.SVC(kernel="poly") #,decision_function_shape='ovo'
    clf.fit(X,Y["cat"])
    return clf

def save_model(model,model_path):
    with open(model_path, "wb") as pickel_outfile:
        pickle.dump(model, pickel_outfile)
    return 

def evalutate_model(model,X_test,y_test):
    y_pred= model.predict(X_test)
    avg = "micro"
    f_score = f1_score(y_pred,y_test,average=avg)
    p_score = precision_score(y_pred,y_test,average=avg)
    r_score = recall_score(y_pred,y_test,average=avg)
    return p_score, r_score, f_score

def main():
    X_train, X_test, y_train, y_test = preprocess(captures_path,test_size=0.25)
    model = train(X_train,y_train)
    precision, recall, f1 = evalutate_model(model,X_test,y_test["cat"])
    print("percision:\t{}".format(precision))
    print("recall:\t\t{}".format(recall))
    print("f1_score:\t{}".format(f1))
    save_model(model,model_path)
    print("training executed")

if __name__ == "__main__":
    #load some information from config.yaml
    config_path = "project\config.yaml"
    with open(config_path, "r", encoding="utf8") as config_file:
        config_info = yaml.safe_load(config_file.read())

    captures_path = config_info["captures_path"]
    model_path = config_info["model_path"]
    
    main()