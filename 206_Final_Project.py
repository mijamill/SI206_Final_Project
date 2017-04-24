##############################################################
# Import Statements
import tweepy
from yahoo_finance import Share
import unittest
import twitter_info
import json
from textblob import TextBlob
import sqlite3
from collections import Counter
import pprint
##############################################################

##############################################################
#Twitter Info Setup To Test Function
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Set up Twitter API
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
##############################################################

##############################################################
# Cache File Info/Setup
CACHE_FNAME = "Final_Project_Cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}
##############################################################

##############################################################
# Class company, created for each instance of company to be searched
class Company():

	def __init__(self, name, stock_symbol, twitter_searches):
		self.name = name
		self.stock_symbol = stock_symbol
		self.list_for_twitter = twitter_searches
		self.stock = Share(stock_symbol)


	def get_tweets_company(self):
		unique_identifier = "tweets_{}".format(self.name)
	
	#If company has already been searched, use Cached Results
		if unique_identifier in CACHE_DICTION:
			self.tweets = CACHE_DICTION[unique_identifier]

		#Get results for company search from API, cache them
		else:
			tweety = api.search(self.list_for_twitter, count = 200, 
                                 include_rts = 1)
			tweety1 = api.search(self.name, count = 200, include_rts = 1)
			self.tweets = tweety['statuses'] + tweety1['statuses']
			CACHE_DICTION[unique_identifier] = self.tweets 
			f = open(CACHE_FNAME,'w') 
			f.write(json.dumps(CACHE_DICTION))
			f.close()

		#Return tweets from either cache or API search
		return self.tweets

	def get_stock_info(self):
		unique_identifier = "stocks_{}".format(self.name)
	
		#If company has already been searched, use Cached Results
		if unique_identifier in CACHE_DICTION:
			self.stock_info = CACHE_DICTION[unique_identifier]

		#Get results for company search from API, cache them
		else:
			stock_info_temp = self.stock.get_historical('2017-04-17', 
                                                         '2017-04-21')
			week_start = stock_info_temp[4]['Close']
			week_end = stock_info_temp[0]['Close']
			self.stock_info = {"Symbol": self.stock_symbol, 
                               "Start_Val": week_start, "End_Val": week_end}
			CACHE_DICTION[unique_identifier] = self.stock_info
			f = open(CACHE_FNAME,'w') 
			f.write(json.dumps(CACHE_DICTION))
			f.close()

		return self.stock_info

##############################################################

##############################################################
# Additional Helper Functions
def get_tweet_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    return analysis.sentiment.polarity

def average(val_pair):
	return(float(val_pair[0])/float(val_pair[1]))

def change(start, end):
	return (((float(end)-float(start))/float(start))*100)
##############################################################

##############################################################
## Class is initalized with Name of company, stock ticker, and list of twitter
## searchable names for the company
company_1 = Company("Rockwell Collins", "COL", "$COL")
company_2 = Company("Mattel", "MAT", "$MAT")
company_3 = Company("Under Armour", "UA", "$UAA")
company_4 = Company("Stanley Black and Decker", "SWK", "$SWK")

#List below will contain all companies that are initialized, just like above
company_list = [company_1, company_2, company_3, company_4]

# For each instance, I will call the get_tweets and get_stock_info methods
## These methods will use provided info to pull stock info and tweets related 
## to the company, and store them in the cache file
for companies in company_list:
	companies.get_tweets_company()
	companies.get_stock_info()

##############################################################


##############################################################
# At this point, I have all my data, and now need to initialize my cursor for 
# the db
conn = sqlite3.connect('Final_Project.db')
cur = conn.cursor()

# Then I will create two tables, Tweets and Stocks
cur.execute('DROP TABLE IF EXISTS Tweets')

table_spec  = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, '
table_spec += 'user TEXT, text TEXT, company TEXT, time_posted TIMESTAMP, '
table_spec += 'retweets INTEGER, Sentiment DECIMAL)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Stocks')

table_spec  = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Stocks (Company TEXT PRIMARY KEY, '
table_spec += 'Week_Start DECIMAL, Week_End DECIMAL, Percent_Change DECIMAL)'
cur.execute(table_spec)

cur.execute('DROP TABLE IF EXISTS Stock_Tweets')

table_spec  = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Stock_Tweets (Company TEXT PRIMARY KEY, '
table_spec += 'Stock_Tweet_Sentiment, Tweets_About_Stock)'
cur.execute(table_spec)


##############################################################

##############################################################
# After info is pulled and database is created, I will then insert all values 
# for each instance of company into corresponding database
statement = 'INSERT INTO Stocks VALUES (?, ?, ?, ?)'
stock_upload = []

for companies in company_list:
	stock_temp = companies.get_stock_info()
	stock_upload.append([companies.name, stock_temp['Start_Val'], 
                         stock_temp['End_Val'], change(stock_temp['Start_Val'],
                         stock_temp['End_Val'])])
	# pprint.pprint(stock_temp)

for s in stock_upload:
		cur.execute(statement, s)

conn.commit()

statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?, ?)'
tweet_upload = []
id_count = 0
for companies in company_list:
	tweets_temp = companies.get_tweets_company()
	for i in range(len(tweets_temp)):
		tweet_upload.append([id_count, tweets_temp[i]['user']['screen_name'], 
                             tweets_temp[i]['text'], companies.name, 
                             tweets_temp[i]['created_at'], 
                             tweets_temp[i]['retweet_count'], 
                             get_tweet_sentiment(tweets_temp[i]['text'])])
		id_count += 1
	# pprint.pprint(tweets_temp)

for t in tweet_upload:
		cur.execute(statement, t)

conn.commit()

statement = "Select company, Sentiment from Tweets"
cur.execute(statement)

sentiment_company = cur.fetchall()
sentiment_by_company = {}
for i in range(len(sentiment_company)):
	if sentiment_company[i][0] not in sentiment_by_company.keys():
		sentiment_by_company[sentiment_company[i][0]] = [sentiment_company[i][1], 1]
	else:
		sentiment_by_company[sentiment_company[i][0]][0] += sentiment_company[i][1]
		sentiment_by_company[sentiment_company[i][0]][1] += 1


statement = 'INSERT INTO Stock_Tweets VALUES (?, ?, ?)'
tweet_upload = []
id_count = 0
Id_val = 0
for companies in company_list:
	tweet_count = 0
	tweets_temp = companies.get_tweets_company()
	check_string = companies.list_for_twitter
	print(check_string)
	sentiment_temp = 0
	for i in range(len(tweets_temp)):
		c = Counter(tweets_temp[i]['text'].split())
		if c[check_string] > 0:
			print("Found " + check_string)
			tweet_count += 1
			sentiment_temp += get_tweet_sentiment(tweets_temp[i]['text'])
		if tweet_count == 0:
			score = None
		else:
			score = average([sentiment_temp, tweet_count])
	tweet_upload.append([companies.name, score, tweet_count])

for t in tweet_upload:
		cur.execute(statement, t)

conn.commit()

##############################################################

##############################################################
# Put your tests here, with any edits you now need from when you turned them 
# in with your project plan.
class Test_Cases(unittest.TestCase):
	def test_cache_file(self):
		fpt = open("Final_Project_Cache.json","r")
		fpt_str = fpt.read()
		fpt.close()
		obj = json.loads(fpt_str)
		self.assertEqual(type(obj),type({"hi":"bye"}))
	def test_get_stock_data(self):
		company_1 =  Company("Target", "TGT", ["Target", "Target Corporation"])
		stock_info = company_1.get_stock_data()
		#Based on function I am planning on using, the data returned should be a list of dictionaries
		self.assertEqual(type(stock_info), type([{'A': 1}, {'B': 2}]))
	def test_get_tweets(self):
		company_1 =  Company("Target", "TGT", ["Target", "Target Corporation"])
		tweet_info = company_1.get_tweet_data()
		self.assertEqual((type(tweet_info), type({'a': "hello"})), "Testing that tweet data is returned in dictionary format")
	def test_tweets_db1(self):
		conn = sqlite3.connect('Final_Project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=1, "Testing that something was stored in the Tweets db")
		conn.close()
	def test_tweets_db2(self):
		conn = sqlite3.connect('Final_Project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Tweets db")
		conn.close()
	def test_stocks_db1(self):
		conn = sqlite3.connect('Final_Project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=1, "Testing that something was stored in the Stocks db")
		conn.close()
	def test_stocks_db2(self):
		conn = sqlite3.connect('Final_Project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==5,"Testing that there are 5 columns in the Stocks db")
		conn.close()
##############################################################

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
# if __name__ == "__main__":
# 	unittest.main(verbosity=2)