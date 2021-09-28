# tweet_screenshot_classifier
currently private! classifies OCR output from tweet screenshots.

## requirements
* [pytesseract](github.com/madmaze/pytesseract)
* [TweetCapture](github.com/Xacnio/tweetcapture)

#### modules (pip install):
* sklearn
* pandas
* Pillow

## usage
setup the config.yaml with your local paths
run inference.py with an image path and get a search link back (CLI implemnted)
run training.py to train the model (CLI interface not available)
run screenshot_handling to generate and annotate more data (CLI interface not available)

## license
MIT
