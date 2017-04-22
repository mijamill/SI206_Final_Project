###### INSTRUCTIONS ###### 

# Name: Michael Miller
# Uniquename: mijamill
# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import tweepy
from yahoo_finance import Share
import unittest
import itertools
import collections
import twitter_info
import json
import textblob
import sqlite3
# Begin filling in instructions....

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

CACHE_FNAME = "Final_Project_Cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# I will first Create instances of Class Company for each company that I will be doing research for
class Company():

	def __init__(self, name, stock_symbol, twitter_searches):
		self.name = name
		self.stock_symbol = stock_symbol
		self.list_for_twitter = twitter_searches
		self.tweets = {}


	def get_tweets_company(self):
	unique_identifier = "tweets_{}".format(self.name)
	
	#If company has already been searched, use Cached Results
	if unique_identifier in CACHE_DICTION:
		self.tweets = CACHE_DICTION[unique_identifier]

	#Get results for company search from API, cache them
	else:
		tweets = api.search(self.name, count = 100, include_rts = 1)
		CACHE_DICTION[unique_identifier] = tweets 
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	#Return tweets from either cache or API search
	return tweets

## Class is initalized with Name of company, stock ticker, and list of twitter searchable names for the company
company_1 = Company("Target", "TGT", ["Target", "Target Corporation"])

#List below will contain all companies that are initialized, just like above
company_list = [company_1]

# For each instance, I will call the get_tweets and get_stock_info methods
## These methods will use provided info to pull stock info and tweets related to the company, and store them in the cache file
for companies in company_list:
	companies.get_tweets()
	companies.get_stock_info()


# At this point, I have all my data, and now need to initialize my cursor for the db
conn = sqlite3.connect('Final_Project.db')
cur = conn.cursor()

# Then I will create two tables, Tweets and Stocks
cur.execute('DROP TABLE IF EXISTS Tweets')

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, '
table_spec += 'text TEXT, user_posted TEXT, time_posted TIMESTAMP, retweets INTEGER)'
cur.execute(table_spec)

# After info is pulled and database is created, I will then insert all values for each instance of company into corresponding database
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'

tweet_upload = []

for companies in company_list:
	tweets_temp = companies.tweets()
	for i in range(len(tweets_temp)):
		tweet_upload.append([tweets_temp[i]['id'], tweets_temp[i]['text'], companies.name, tweets_temp[i]['created_at'], tweets_temp[i]['retweet_count']])

for t in tweet_upload:
		cur.execute(statement, t)

conn.commit()

# join these data bases by company name
statement = "select * from db1.Tweets a inner join db2.Stocks b on b.Tweets = a.Companies"

cur.execute(statement)

data_from_db = cur.fetchall()
# Finally, I will do three sepearte pulls of data, and store it in csvs which will then allow me to visualize the data in tableau


# Put your tests here, with any edits you now need from when you turned them in with your project plan.
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


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)