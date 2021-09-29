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
    # via https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_tweet_link(input_id): 
    """
    takes a tweet_id and returns the correct url (inlcuding username) using the twitter api. (might only work for 7 days)
    
    args: 
        input_id (int): tweet ID
    return:
        output_url (str): full link including user/status/tweet_id
    errors:
        tweet not found (incorrect raise): if tweet_id doesn't have an exsisting tweet anymore.
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

    args:
        returns (int): number of tweet_ids returned

    returns:
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
    # print(json.dumps(tweet_lookup(sample_stream_ids(1)[0]), indent=4, sort_keys=True))  
    print("main executed")

if __name__ == "__main__":
    #load some information from config.yaml
    config_path = "project\config.yaml"
    with open(config_path, "r", encoding="utf8") as config_file:
        config_info = yaml.safe_load(config_file.read())

    bearer_token = config_info["bearer_token"]
    language = config_info["lang"]
    
    main()

