sample-python-autoreply
===

Simple auto-reply using Python and Tweepy. Replies with same Tweet text.

To run this sample code, you'll need to install the following python libraries:

- Tweepy: [https://github.com/tweepy/tweepy](https://github.com/tweepy/tweepy)
- NLTK: [http://www.nltk.org/](http://www.nltk.org)


GETTING STARTED
---
Create a [Twitter App](https://apps.twitter.com/).

Specify your Twitter App keys and tokens in a new config file named .twitter. There is a sample config file named .twitter.sample:

```
[apikey]
key = your_api_key
secret = your_api_secret

[token]
token = your_access_token
secret = your_access_secret

[app]
rule = @AccountOwnerOfApp
account_screen_name = AccountOwnerOfApp
account_user_id = UserIdOfAccountOwner

```

Install dependencies:

```
pip install tweepy nltk
```

Run the python script in the project directory:

```
python AutoResponse.py
```
