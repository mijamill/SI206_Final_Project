## Commented code used in order to test function for completion
# import tweepy
# from yahoo_finance import Share
# import unittest
# import itertools
# import collections
# import twitter_info
# import json
# import sqlite3

# #Twitter Info Setup To Test Function
# consumer_key = twitter_info.consumer_key
# consumer_secret = twitter_info.consumer_secret
# access_token = twitter_info.access_token
# access_token_secret = twitter_info.access_token_secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# #Set up Twitter API
# api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# CACHE_FNAME = "Final_Project_Cache.json"

# try:
# 	cache_file = open(CACHE_FNAME,'r')
# 	cache_contents = cache_file.read()
# 	cache_file.close()
# 	CACHE_DICTION = json.loads(cache_contents)
# except:
# 	CACHE_DICTION = {}


# company_handle used for actual twitter search, company name used for cache
# Code used from numerous homeworks involved with tweet data
def get_tweets_company(company_name):
	unique_identifier = "tweets_{}".format(company_name)
	
	#If company has already been searched, use Cached Results
	if unique_identifier in CACHE_DICTION:
		tweets = CACHE_DICTION[unique_identifier]

	#Get results for company search from API, cache them
	else:
		tweets = api.search(company_name, count = 5, include_rts = 1)
		CACHE_DICTION[unique_identifier] = tweets 
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	#Return tweets from either cache or API search
	return tweets


##Code below used for testing

#tweet_get = get_tweets_company("Target")

#print(tweet_get)