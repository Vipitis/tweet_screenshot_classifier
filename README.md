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
1. run inference.py with an image path and get a search link back (CLI implemnted)
2. run screenshot_handling to generate and annotate more data (CLI not available)
3. run training.py to train the model (CLI not available)

## license
MIT
