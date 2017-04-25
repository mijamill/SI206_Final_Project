READEME

Project Title
-----------------------------------------------------------------------------------------
This is a readme file for opton 3 of the SI 206 final project.

What This Project Does
-----------------------------------------------------------------------------------------
This project attempts to find the correlation between tweet sentiment and Stock performance. It searches through Yahoo Finance API to pull trends in stock data, and searches twitters API for tweets about those companies. It then creates databases and tables that allows the user to analyze the potnetial correlation for tweets and stocks.

How To Run
-----------------------------------------------------------------------------------------This code is run simply by calling the 206_Final_Project.py file. If you have not already, you must install the yahoo finance api, the twitter api, and the textblob api (used for sentiment analysis of tweets). Furthermore, you must have a twitter_handle and authorization. This will allow you to use Twitter's api (Search twitter api for more information). Once you have this information, store it in a file named twitter_info.py. This is the only other file that is linked to the main file and will need the information there to run.

Explanation of Class and Functions
-----------------------------------------------------------------------------------------
Start: Line 48
End: Line 98

Class Company
- This class is key to this project. When starting, the code creates instances of each company, which store key information on the company, including the company name and stock symbol

__init__
- Here, the company instance is initalized with the company name, stock symbol, and any other names that may be used to search through twitter for that company. ALl of those are inputs to the intializer

get_tweets_company
- this function takes nothing as input. It uses the company name, stock symbol, and twitter searches from the init function and searches twitter for tweets relating to that company with any of the search terms. It takes the information from the tweets and caches them as well as returning them.

get_stock_info
- this function also takes no input, and uses the stock symbol from init in order to search Yahoo Finance API for information on that given stock. It caches the given data as well as returning it

Other Functions
-----------------------------------------------------------------------------------------
Start: Line 106
End: Line 114

get_tweet_sentiment
-Takes a text string as input, uses TextBlob api to run sentiment analysis, and returns the value of the seniment (betwen 1 and -1)

change
- this takes a starting and ending value and calculates the percentage change of those two values. It returns this in percentage form, and is used to figure out the percent change in stock price for a given stock.

Database - Final Project
-----------------------------------------------------------------------------------------
Start: Line 143
End: Line 167

Table - Tweets
Col 0 - TweetID
- Unique id for each tweet to satisfy sql requirement
Col 1 - User
-Text Column in which the username of the person for the given tweet is stored
Col 2 - Text
- Text column in which the text for the specific tweet is stored
Col 3 - TimePosted
- TimeStamp column in which the time the tweet was created is stored
Col 4 - Retweets
- Integer column in which the number of retweets for that tweet is stored
Col 5 - Sentiment
- Decimal column where the sentiment score for each tweet is stored

Table - Stocks
Col 0 - Company
- Text column to store name of company
Col 1 - Week_Start
- Decimal column to show the starting value of the stock price for the week
Col 2 - End_Val
- Decimal column to show the ending value of the stock price for the week
Col 3 - Percent_Change
- Decimal column showing the percent change between the start and end values

Table - Stock_Tweets
Col 0 - Company
- Text column to store name of company
Col 1 - Stock_Tweet_Sentiment
- Decimal column to store collective value of sentiment for tweets about stocks
Col 2 - Tweets_About_Stock
- Integer column showing a count of the amount of tweets which speficially refernce the stock
Col 3 - Tweets_About_Company
- Integer column to store total tweets about a company

Data Manipulation
-----------------------------------------------------------------------------
Counter (Line: 234-236)
- A counter is uesd to figure out how many tweets specifically reference the stock. This information is useful in determing twitter sentiment about stocks specifically referencing the stock itself as opposed to general tweets about the company

Dictionary Accumulation (Line: 211-220)
- This is used to figure out the sentiment of tweets for a company as a whole. Storing the company name as a key in a dictionary, the code can go through and accumulate total sentiment score for each tweet and then average it out using the functions provided.

Reduce (Line: 239)
- This generator function is used to find the average of sentiment for tweets relating to specific stocks and then applies it to the Stock_Tweets database

TextBlob (Line: 107)
- This is used to calculate sentiment for tweets. It takes a built in list of words to do sentiment analysis and then returns a score.

Summary
-----------------------------------------------------------------------------
I choose this project because I have always had a strong interest in business. Recently, I have also developed a strong intrest and trends and anlyatics. I was curious to see if a trend could be found between the tweet sentmient and stock trends. The goal and output of this project is to allow a user to pick any companies they choose, wheter it be ina certain industry or just be of particualr interest, and find out if tweet sentiment and stock trend are correlated.

Citations
-------------------------------------------------------------------------
SI 206 Project 3
Textblob documentation: http://textblob.readthedocs.io/en/dev/quickstart.html
Yahoo Finance Documentation: https://pypi.python.org/pypi/yahoo-finance
