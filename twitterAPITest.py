import tweepy
import time
import array as arr
import json
from pymongo import MongoClient, ASCENDING
import ssl
from pprint import pprint


consumer_key = "me7t8gR3IK0scAlt3qAF6vZdg"
consumer_secret = "6FG1JsDDJ4bShWmbPUrFb3wT7DcuS8KwYGyer30x44apMmgnuj"
access_token = "820549471-3l5LATlq0nIxO04xICHY0aZWD3xmDU32mY1VvUbj"
access_token_secret = "47e4qFZAjcL0UK7rYDj1Os5ZSmShbNdVhHBtkEos4oART"

# Initialize the Cosmos client
ENDPOINT = "mongodb://cs2s:27017/?authSource=gregoryswedeen&gssapiServiceName=mongodb"
PORT = 27017
client = MongoClient(ENDPOINT, PORT, username='gregory.swedeen', password='TN4H4SFJ',) 

#Select the database
db = client.testDatabase   
# Collections 
Trends = db.Trends
tweets = db.tweets

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth informations
api = tweepy.API(auth, wait_on_rate_limit=True) 

# Get Tweets near the users start Location Save in MongoDB
def getTweets(lat, lang):
   tweets.remove({})
   language = 'en'
   radius = '10km'
   print(lat,lang)
   geocode = (str(lat)+','+str(lang)+','+'20km')
   results = api.search(q='*', lang=language, rpp=50, geocode=geocode) #search for tweets that match query
   for tweet in results:
      #save the last tweet searched
      tweetJson = {
         "created_at": tweet.created_at.isoformat() ,
         "tweetID": tweet.id_str ,
         "text": tweet.text,
      }
      item = tweets.find({ 'tweetID': tweetJson['tweetID']})
      if item.count() == 0:
         tweets.insert_one(tweetJson) 

#Get the WOEID necessary for searching for Trends
def getWoeid(lat, lang):
   result = api.trends_closest(lat, lang)
   print(result[0]['woeid'])
   return(result[0]['woeid'])

# Search for Trends
def trendsByPlace(lat,lang):
   trends = api.trends_place(getWoeid(lat,lang))
   trendList = []
   i=0
   while i != 5:
      trend = {
         'name': trends[0]['trends'][i]['name']
      }
      Trends.insert_one(trend)
      i+=1
   return trendList
