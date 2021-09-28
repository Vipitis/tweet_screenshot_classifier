# via https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

import requests 
import json
import re
import yaml
from pathlib import Path

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_tweet_link(input_id): 
    """
    takes a tweet_id and returns the correct url (inlcuding username) using the twitter api. (might only work for 7 days)
    
    Param: 
    input_id : int
        tweet id 
    Return:
    output_url : str
        full rul to tweet including username
    """
    tweet_fields = "expansions=author_id&user.fields=username"
    url = "https://api.twitter.com/2/tweets?ids={}&".format(input_id)
    # print(url)
    json_response = connect_to_endpoint(url,tweet_fields)
    if "errors" in json_response:
        return "Error detected for id {}".format(input_id)
    output_url = "https://twitter.com/{}/status/{}".format(json_response["includes"]["users"][0]["username"],json_response["data"][0]["id"])
    # output_url = str(json_response["data"][0]["id"])
    return output_url

def tweet_lookup(input_id):
    tweet_fields = {"tweet.fields":"source,public_metrics,created_at","expansions":"author_id","user.fields":"username,name,verified"}
    # tweet_fields = "tweet.fields=source,public_metrics&expansions=author_id&user.fields=username,verified"
    url = "https://api.twitter.com/2/tweets?ids={}&".format(input_id)
    json_response = connect_to_endpoint(url,tweet_fields)
    if "errors" in json_response:
        raise "Tweet not found error"
    return json_response

def load_lookup(filepath):
    """
    loads a saved json or generates it viat he tweet_id
    """
    if Path(filepath).exists() == False:
        json_data = tweet_lookup(filepath.stem)
    else: 
        with open(filepath, "r", encoding = "utf8") as json_infile:
            json_data = json.load(json_infile)
    return json_data

def save_lookup(in_json, filepath):
    with open(filepath, "w", encoding= "utf-8") as json_outfile:
        json.dump(in_json, json_outfile)
    return

def generate_tweet_ids(query, max_returns=10, verified=False): #depricated. keeping for reference right now.
    """
    quesries the twitter api recent serach and returns up to 100 tweet ids based on supplied query.

    Params:
        query (str): word or phrase that is looked for
        max_returns (int): min10, max100; upper limit on returns.
        verified (bool): (optional) will return only tweets from verified users if true.

    Returns:
        output_list (list): list of tweet_ids, can be empty if query returns nothing.
    """
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    tweet_text = query

    tweet_author = ""

    if max_returns > 100:
        max_responses = 100
    elif max_returns < 10:
        max_responses = 10
    else: 
        max_responses = max_returns

    search_query = tweet_text + ' -has:media -emoji -is:reply -is:retweet lang=en'

    if len(tweet_author) > 0:
        search_query = 'from:' + tweet_author + ' ' + search_query

    query_params = {'query': search_query ,'tweet.fields': 'author_id,created_at,source,public_metrics,lang,conversation_id', 'expansions':'author_id', 'max_results': max_responses} #'user.fields': 'verified',
    
    json_response = connect_to_endpoint(search_url, query_params)
    tweet_list = []
    for tweet in json_response["data"]:
        tweet_list.append(tweet["id"])
    return tweet_list

def search_tweet_recent(query,author,source=None): #WIP
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    query_params = " ".join(query)
    result_ids = []
    json_response = connect_to_endpoint(search_url, query_params)
    return result_ids

def search_tweet_by_author(author, text): # not working right now...
    """
    if a valid username was found, it tries to search the tweet by text.
    if not it returns and error? - or tries other means - maybe return a url for autocorrect

    """
    author_url = "https://api.twitter.com/2/users/by/username/:" + author
    author_response = connect_to_endpoint(author_url, {"user.fileds: id"})
    # author_id = author_response["data"]["id"]
    return author_response
    # # text_str = " ".join(text)
    # search_url = "https://api.twitter.com/2/users/{}/tweets".format(author_id)

    # query_params = {"tweet.fields": "created_at"}
    # json_response = connect_to_endpoint(search_url, query_params)

    # tweet_id = json_response["data"]["id"]
    # return tweet_id

def generate_search_url(authors, text):
    exp = re.compile("@.")
    if not authors:
        author = ""
    else:
        author = "from%3A" + [e for e in authors if exp.match(e)][0].lstrip("@")
    search_url = "https://twitter.com/search?q={}%20{}&src=typed_query".format(author,requests.utils.quote(" ".join(text)))
    return search_url

def sample_stream_ids(returns):
    """
    uses the twitter sampled stream and returns a list of tweets ids as specified.

    Params:
        returns (int): number of tweet_ids returned\

    Returns:
        output_list (list): list of tweet ids

    """
    
    sample_url = "https://api.twitter.com/2/tweets/sample/stream"
    sample_params = {"tweet.fields": "created_at,lang,possibly_sensitive,referenced_tweets,entities", "media.fields": "type"}

    output_list = []

    response = requests.get(sample_url, auth=bearer_oauth, stream=True, params=sample_params)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response["data"]["lang"] == language \
            and json_response["data"]["possibly_sensitive"] == False \
            and "referenced_tweets" not in json_response["data"] \
            and "urls" not in json_response["data"]["entities"]:
                # print(json.dumps(json_response, indent=4, sort_keys=True))                        
                output_list.append(json_response["data"]["id"])
                returns -= 1
        if returns == 0:
            response.close()
            break 

    return output_list

def main():
    # print()
    print(search_tweet_by_author("jack",["settin","up"]))

    # print(json.dumps(tweet_lookup(sample_stream_ids(1)[0]), indent=4, sort_keys=True))  
    print("main executed")

if __name__ == "__main__":
    #load some information from config.yaml
    config_path = "config.yaml"
    with open(config_path, "r", encoding="utf8") as config_file:
        config_info = yaml.safe_load(config_file.read())

    bearer_token = config_info["bearer_token"]
    language = config_info["lang"]
    
    main()

