
consumer_key='nFVDdbH8tx6u4r0EChGjzICaM'
consumer_secret='QwHBA2tS4mHWgEFAE4CiaIGITX1YkN1OdWLC47dcHVmKFnZYCm'
access_token='25576887-kzTf8H5VMZMkqshhTMlBoa5b4PxrXWewADeNOTyxK'
access_token_secret='gnSu99KKNdFY8VRPZ1dFGNcfZioTcD77y1zmNMKOpX9gL'

#Import the necessary methods from tweepy library
# The code is modified from the following links
# http://adilmoujahid.com/posts/2014/07/twitter-analytics/
# Streaming API requesting parameters: https://dev.twitter.com/streaming/overview/request-parameters#language

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import sys
import json
print 'usage: python twitter_tap.py keyword1 keyword2'

database = []
database_filename = 'people.txt'
database_file = open(database_filename, 'r+')
for line in database_file:
    database.append(line[:-1])

database_file.close()
print database



t = time.time()
timeout = 3600


tweets = []

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            obj = json.loads(data)
            tweettext = obj['text'].replace('\n',' ')
            if tweettext[:3] == "RT ":
               return True
            if "https" in tweettext:
               return True
            if obj['in_reply_to_screen_name'] is None:
                return True
            print obj['user']['screen_name']+": "+tweettext
            print data
            #print obj['user']['screen_name']+" to "+obj['in_reply_to_screen_name']+": "+tweettext
            #tweets.append(obj)
        except KeyError:
            return True
        if time.time()-t>timeout:
            return False
        return True
    

    def on_error(self, status):
        print "twepy error: ",status

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    
    stream.filter(track=sys.argv[1:] , languages=['en']) # <= here is the language filter issue

