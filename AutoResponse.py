import ConfigParser
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import nltk.chat

config = ConfigParser.ConfigParser()
config.read('.twitter')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
stream_rule = config.get('app', 'rule')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

chatbot = eliza.Chat(eliza.pairs)

class ReplyToTweet(StreamListener):

    def on_data(self, data):
        
        print data

        jsonData = json.loads(data.strip())

        friends = jsonData.get('friends')
        if friends:
            # preamble
            # https://dev.twitter.com/docs/streaming-apis/messages#Friends_lists_friends
            print 'Preamble received.'
            return

        if jsonData.get('in_reply_to_status_id'):
            # ignore reply tweets
            print 'Ignoring reply Tweet.'
            return

        tweetId = jsonData.get('id_str')
        screenName = jsonData.get('user').get('screen_name')
        userId = jsonData.get('user').get('id')
        tweetText = jsonData.get('text')

        replyText = chatbot.respond(tweetText);
        
        print('Tweet ID: %s' % tweetId)
        print('Screen Name: %s' % screenName)
        print('User ID: %s' % userId)
        print('Tweet Text: %s' % tweetText)
        print('Reply Text: %s' % replyText)
        print('')

        # If rate limited, the status posts should be queued up and sent on an interval
        #twitterApi.update_status(replyText, tweetId)

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    r = ReplyToTweet()
    twitterStream = Stream(auth, r)
    twitterStream.userstream(track=[stream_rule])