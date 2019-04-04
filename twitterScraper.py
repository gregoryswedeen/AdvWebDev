import tweepy
import array as arr
import json
from pymongo import MongoClient
import sys

consumer_key = "me7t8gR3IK0scAlt3qAF6vZdg"
consumer_secret = "6FG1JsDDJ4bShWmbPUrFb3wT7DcuS8KwYGyer30x44apMmgnuj"
access_token = "820549471-3l5LATlq0nIxO04xICHY0aZWD3xmDU32mY1VvUbj"
access_token_secret = "47e4qFZAjcL0UK7rYDj1Os5ZSmShbNdVhHBtkEos4oART"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True) 

#print(api.VerifyCredentials())



#PARAMETERS
minimumFollowerCount = 2000 #Minimum follower count to be considered

queries = []
queries.append("Weather")
queries.append("Snow")

followers = []
accounts = []

accounts.append("WSJ")

searchedAccounts = []
account = "WSJ"





def getUserInfo():  
   j = 0
   account = accounts[j]
   info = []

   for j in accounts:
      userInfo = {
         "screen_name": account,
         "created_at": returnCreatedAt(account).isoformat(),
         "isProtected": returnIsProtected(account),
         "isVerified": returnIsVerified(account),
         "tweet_count": returnTweetCount(account),
         "follower_count": returnFollowerCount(account)
      }
      info.append(userInfo)

   y = json.dumps(info,indent=4, sort_keys=True, default=str)

   return y

def keywordSearch(): #Returns list of search results
    i=0
    while i < len(queries):
    
        JsonTweets = []
        tweets = []
        # The search term you want to find
        query = queries[i]
        # Language code (follows ISO 639-1 standards)
        language = "en"
        locale = "Boston"
        #rpp = '100' (response per page)
        #page = "10" (number of pages of response)
        #since_id = "_____" 
        #geocode = "______"
        #show_user (adds the users name onto the front of the Tweet)

        # Calling the user_timeline function with our parameters
        results = api.search(q=query, lang=language, locale=locale)
        tweets.extend(results)
        oldest = tweets[-1].id - 1
        


        while len(results) > 0:
            #all subsequent requests use the max_id param to prevent duplicates
            results = api.search(q=query, lang=language, locale=locale, since_id = oldest, max_id=oldest)
            #save most recent tweets
            tweets.extend(results)
            #update the id of the oldest tweet minus one
            oldest = tweets[-1].id - 1

        #TRIM TAGS
        for tweet in tweets:

            retweets = api.retweeters(tweet.id)

            tweetJson = {
                "created_at": tweet.created_at.isoformat() ,
                "tweetID": tweet.id_str ,
                "account": tweet.user.screen_name ,
                "text": tweet.full_text ,
                "retweet_count": tweet.retweet_count ,
                "favorite_count": tweet.favorite_count,
                "in_reply_to_screen_name": tweet.in_reply_to_screen_name,
                "in_reply_to_status_id_str": tweet.in_reply_to_status_id_str,
                "coordinates": tweet.coordinates,
                "retweeted_by": retweets
                },
        
            JsonTweets.append(tweetJson)

        File = json.dumps(JsonTweets,indent=4, sort_keys=True)
        print(File)

def getFollowers():
   #Name of account
   name = "WSJ"

   #get the followers for the account name
   results = api.followers(id = name)

   for user in results:
      id = user.id
      followers.append(id)

   y = json.dumps(followers,indent=4, sort_keys=True, default=str)

   #for users in the results, only print the screen name of each user
   print(y)

def searchUsers(): #creates list of users that match criteria
   #Query for users related to subject, also use per_page and page
   i = 0
   while i != (len(queries)):   #search users for every query
      query = queries[i]
      i += 1
      per_page = 20
      page = 0

      while page <= 50: #retrieve max number of search results
         results = api.search_users(q = query, per_page = per_page, page = page)
         page += 1
      #    #save most recent accounts
         for user in results: 
            if user.screen_name not in searchedAccounts: #make sure they arent a duplicate
               if returnFollowerCount(user.screen_name) > minimumFollowerCount:  #make sure they have enough followers
                  searchedAccounts.append(user.screen_name)
   print(searchedAccounts)  
   print(len(searchedAccounts))   

def getAllTweets(): #retrieve last 3000 tweets
   JsonTweets = []
   id = account
   tweets = []
   results = api.user_timeline(screen_name = id, count = 200, tweet_mode="extended")
   tweets.extend(results)
   oldest = tweets[-1].id - 1

   while len(results) > 0:
      #all subsequent requests use the max_id param to prevent duplicates
      results = api.user_timeline(screen_name = id,count=200,max_id=oldest, tweet_mode="extended")
      #save most recent tweets
      tweets.extend(results)
      #update the id of the oldest tweet minus one
      oldest = tweets[-1].id - 1

   #TRIM TAGS
   for tweet in tweets:

      retweets = api.retweeters(tweet.id)

      tweetJson = {
            "created_at": tweet.created_at.isoformat() ,
            "tweetID": tweet.id_str ,
            "account": tweet.user.screen_name ,
            "text": tweet.full_text ,
            "retweet_count": tweet.retweet_count ,
            "favorite_count": tweet.favorite_count,
            "in_reply_to_screen_name": tweet.in_reply_to_screen_name,
            "in_reply_to_status_id_str": tweet.in_reply_to_status_id_str,
            "coordinates": tweet.coordinates,
            "retweeted_by": retweets
            },
      
      JsonTweets.append(tweetJson)

   File = json.dumps(JsonTweets,indent=4, sort_keys=True)
   print(File)

def returnFollowerCount(account):   #Returns Follower Count when passed an account
   id = account
   results = api.get_user(id = id)

   followerCount = results.followers_count
   return followerCount

def returnCreatedAt(account):   #Returns Follower Count when passed an account
   id = account
   results = api.get_user(id = id)

   createdAt = results.created_at
   return createdAt

def returnLocation(account):   #Returns Follower Count when passed an account
   id = account
   results = api.get_user(id = id)

   location = results.location
   return location

def returnIsVerified(account):   #Returns Follower Count when passed an account
   id = account
   results = api.get_user(id = id)

   verified = results.verified
   return verified

def returnIsProtected(account):   #Returns Follower Count when passed an account
   id = account
   results = api.get_user(id = id)

   protected = results.protected
   return protected

def returnTweetCount(account):   #Returns Follower Count when passed an account
   id = account
   results = api.get_user(id = id)

   tweetCount = results.statuses_count
   return tweetCount

def tweetInfo(id):
   results = api.get_status(id = id, tweet_mode="extended")

   print(results)

#searchUsers()

#getAllTweets()

#getUserInfo()

#getAllTweets()
keywordSearch()


#getFollowers()
#storeTweets()

