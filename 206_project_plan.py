## Your name: Michael Miller
## The option you've chosen: 3

# Put import statements you expect to need here!

import tweepy
from yahoo_finance import Share
import unittest
import itertools
import collections
import twitter_info
import json
import sqlite3


# Write your test cases here.

class Test_Cases(unittest.TestCase):
	def test_cache_file(self):
		fpt = open("Final_Project_Cache.json","r")
		fpt_str = fpt.read()
		fpt.close()
		obj = json.loads(fpt_str)
		self.assertEqual(type(obj),type({"hi":"bye"}))
	def test_get_stock_data(self):
		stock_info = get_stock_data("Target")
		#Based on function I am planning on using, the data returned should be a list of dictionaries
		self.assertEqual(type(stock_info), type([{'A': 1}, {'B': 2}]))
	def test_get_tweets(self):
		tweet_info = get_tweet_data("Target")
		self.assertEqual((type(tweet_info), type({'a': "hello"})), "Testing that tweet data is returned in dictionary format")
	def test_tweets_db1(self):
		conn = sqlite3.connect('Final_Project_Tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=1, "Testing that something was stored in the Tweets db")
		conn.close()
	def test_tweets_db2(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Tweets db")
		conn.close()
	def test_stocks_db1(self):
		conn = sqlite3.connect('Final_Project_Stocks.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=1, "Testing that something was stored in the Stocks db")
		conn.close()
	def test_stocks_db2(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==5,"Testing that there are 5 columns in the Stocks db")
		conn.close()


if __name__ == "__main__":
	unittest.main(verbosity=2)
