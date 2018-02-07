from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:sec-002
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
# url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
# requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:

#Code for Part 3:Caching----------------------------------------------------------------
#Finish parts 1 and 2 and then come back to this
#using code from class
# on startup, try to load the cache from file
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params, auth):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        pass ## it's a cache miss, fall through to refresh code

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file

    print("Making a request for new data...")
    # Make the request and cache the new data
    resp = requests.get(baseurl, params, auth=auth)
    CACHE_DICTION[unique_ident] = json.loads(resp.text)
    dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]

# # Gets data from the twitter API, using the cache
# def get_tweet_from_caching(username):
#     baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
#     params_diction = {}
#     params_diction["screen_name"] = username
#     params_diction["count"] = num_tweets
#     return make_request_using_cache(baseurl, params_diction)

#extract just the 'text' from the data structures returned by twitter api
def get_text_list(tweet_dict_list):
    atweet = []
    for adict in tweet_dict_list:
        atweet.append(adict['text'])
    return atweet

def get_tweet(username, num_tweets, auth):
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'screen_name': username, 'count': num_tweets}
    return make_request_using_cache(base_url, params, auth)

def tweet_token(alist_with_text):
    tweet_tokenize = []
    for sentence in alist_with_text:
        tweet_tokenize.append(nltk.tokenize.word_tokenize(sentence))
    return tweet_tokenize

def filted_freqDist(tokenizedList):
    stop_words = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_dist = nltk.FreqDist()
    for tokened_sen in tokenizedList:
        for token in tokened_sen:
            if token not in stop_words and token.isalpha():
                freq_dist[token.lower()] += 1
    return freq_dist

#Code for Part3 Ends----------------------------------------------------------------------------

#Code for Part 1:Get Tweets--------------------------------------------------------------------
def part1():
    base_url_part1 = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    response_part1 = requests.get(base_url_part1, {'screen_name': username, 'count': num_tweets}, auth = auth).json()
    #create tweet.json file
    with open('tweet.json', 'w') as outfile:
        json.dump(response_part1, outfile, ensure_ascii=False, indent=4)
#Code for Part 1 Ends--------------------------------------------------------------------------

##Code for Part 2:Analyze Tweets-----------------------------------------------------------------
##using tweet.json file--------------------------------
def part2_with_jsonfile():
    with open('tweet.json') as json_data:
        tweet_data = json.load(json_data)
        json_data.close()
        # print(tweet_data)

    tweet_text = []
    for adict in tweet_data:
        tweet_text.append(adict["text"])
    atweet_token = []
    for sentence in tweet_text:
        atweet_token.append(nltk.tokenize.word_tokenize(sentence))

    stop_words = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_dist = nltk.FreqDist()
    for tokened_sen in atweet_token:
        for token in tokened_sen:
            if token not in stop_words and token.isalpha():
                freq_dist[token] += 1
    print(freq_dist.most_common(5))
##end for using tweet.json file------------------------

#get data from twitter API----------------------------
def part2_with_api():
    base_url_part2 = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    response_part2 = requests.get(base_url_part2, {'screen_name': username, 'count': num_tweets}, auth = auth).text
    tweetDictList_part2 = json.loads(response_part2)

    tweetText_part2 = []
    try:
        for adict in tweetDictList_part2:
            tweetText_part2.append(adict["text"])
    except:
        print('Oops! The username is not valid, Please try a different one. :)')
        quit()
    tweet_token_part2 = []
    for sentence in tweetText_part2:
        tweet_token_part2.append(nltk.tokenize.word_tokenize(sentence))

    stop_words_part2 = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_dist = nltk.FreqDist()
    for tokened_sen in tweet_token_part2:
        for token in tokened_sen:
            if token not in stop_words_part2 and token.isalpha():
                freq_dist[token] += 1


    print('----------**Result for Part 2**----------')
    print(freq_dist.most_common(5))
    print('-----------------------------------------')
#get data from twitter API Ends--------------------------


##Code for Part 2 Ends.-------------------------------------------------------------------------

if __name__ == "__main__":
    def part3():
        if not consumer_key or not consumer_secret:
            print("You need to fill in client_key and client_secret in the secret_data.py file.")
            exit()
        if not access_token or not access_secret:
            print("You need to fill in this API's specific OAuth URLs in this file.")
            exit()

        print('----------**Result for Part 3**----------')
        tweet_whole_dictList = get_tweet(username, num_tweets, auth)
        try:
            tweet_text_list = get_text_list(tweet_whole_dictList)
        except:
            print('Oops! Invalid username! Please try a different one. :)')
            quit()
        if tweet_text_list != []:
            tokenized_list = tweet_token(tweet_text_list)
            print(filted_freqDist(tokenized_list).most_common(5))
        print('-----------------------------------------')

    # part1()
    # part2_with_jsonfile()
    # part2_with_api()
    part3()

    
