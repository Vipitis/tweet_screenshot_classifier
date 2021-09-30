# tweet_screenshot_classifier
currently private! classifies OCR output from tweet screenshots.

## requirements
* [pytesseract](github.com/madmaze/pytesseract)
* [TweetCapture](github.com/Xacnio/tweetcapture) (and it's requirements)
* twitter API access (for generating and annotating screensshots)

#### modules (pip install):
* requests 
* sklearn
* pandas
* Pillow

## usage
setup the config.yaml with your local paths and bearer token
unpack the training data to use it
1. run inference.py with an image path and get a search link back (CLI implemnted)
```
>inference.py
usage: inference.py [-h] [-p] [-t] [input_img]

positional arguments:
  input_img    path to an .png image of a tweet screenshot. If none is given, it will run as -t

optional arguments:
  -h, --help   show this help message and exit
  -p, --preds  prints prediced name, author, text, source
  -t, --test   ignores input and tries a random screenshot from the tests folder
```

3. run screenshot_handling to generate and annotate more data (CLI not available)
4. run training.py to train the model (CLI not available)

## license
MIT
