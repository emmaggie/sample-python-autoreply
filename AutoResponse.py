import ConfigParser
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

from nltk.chat import eliza

config = ConfigParser.ConfigParser()
config.read('.twitter')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
stream_rule = config.get('app', 'rule')
account_screen_name = config.get('app', 'account_screen_name').lower() 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

chatbot = eliza.Chat(eliza.pairs)

class ReplyToTweet(StreamListener):

    def on_data(self, data):

        jsonData = json.loads(data.strip())

        # preamble - https://dev.twitter.com/docs/streaming-apis/messages#Friends_lists_friends
        friends = jsonData.get('friends')
        if friends:
            print 'Preamble received.'
            return

        # deletes - deleting a Tweet will broadcast through the stream
        delete = jsonData.get('friends')
        if delete:
            print 'Ignoring delete.'
            return

        # ignore Tweets from the app owner account
        screenName = jsonData.get('user').get('screen_name')
        if screenName.lower() == account_screen_name:
            print 'Ignoring my own Tweets.'
            return

        tweetId = jsonData.get('id_str')
        tweetText = jsonData.get('text')

        replyText = '@' + screenName + ' ' + chatbot.respond(tweetText)

        if len(replyText) > 140:
            replyText = replyText[0:137] + '...'

        print('Tweet ID: ' + tweetId)
        print('From: ' + screenName)
        print('Tweet Text: ' + tweetText)
        print('Reply Text: ' + replyText)

        # If rate limited, the status posts should be queued up and sent on an interval
        twitterApi.update_status(replyText, tweetId)


    def on_error(self, status):
        print status


if __name__ == '__main__':
    r = ReplyToTweet()
    twitterStream = Stream(auth, r)
    twitterStream.userstream(track=[stream_rule])