import feedparser
from requests_oauthlib import OAuth1Session
import time
import os
import pendulum
import json


#This function can only be used with a developer account so we can generate all keys (consumer and access keys) needed for the twitter API. the output is an OAuth session with which we can tweet.
def get_oauth_object():
    with open('secret.json') as secret:
        js= json.load(secret)
    consumer_key = js['consumer_key']
    consumer_secret =js['consumer_secret']
    access_token = js['access_token']
    access_token_secret = js['access_token_secret']

    oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)
    return oauth

#Function through which we obtain the credentials of any user, requiring their authorization. the output is an OAuth session with which we can tweet
def get_credentials_from_scratch():

    #Consumer Keys that represents the app. They MUST be in the environment and not in the code when the app is in production.
    with open('secret.json') as secret:
        js= json.load(secret)
    consumer_key = js['consumer_key']
    consumer_secret =js['consumer_secret']

    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    #Get request token (these tokens can be used for tweeting on behalf of the user, but at first they're disabled)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    #Get authorization. In this step the user authorizes our app. the users logs in using the url provided by the app and then inserts the PIN
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)
    return oauth

def get_rss(last_modified):
    d= feedparser.parse('https://udc.es/es/rss/fontesRSS/especificas/rss_ori.xml', modified=last_modified)
    if d.status != 304:
        tweets = []
        for item in d.entries:
            if last_modified is None or len(last_modified)==0:
                tweets.append({'title': item.title,
                            'url': item.link})
            elif pendulum.from_format(last_modified, "ddd, DD MMM YYYY HH:mm:ss z") < pendulum.from_format(item.published, "ddd, DD MMM YYYY HH:mm:ss Z"):
                tweets.append({'title': item.title,
                            'url': item.link})
        last_modified = d.modified
        with open('last_modified_rss','w') as file:
            file.write(last_modified) # We persist the date so, in case the script stops and needs to be re-executed again, it won't receive old items
        return last_modified, tweets
    else: 
        print('No new items')
        return last_modified, None

def tweet(oauth, tweet):
         response = oauth.post(
         "https://api.twitter.com/2/tweets",
         json={'text': tweet['title'] + ' ' + tweet['url'] },
    )

if __name__ == "__main__":
    last_modified= None
    if os.path.isfile('last_modified_rss'):
        with open('last_modified_rss') as file:
            last_modified = file.read()
    oauth = get_credentials_from_scratch()
    while True:
        last_modified, tweets= get_rss(last_modified)
        if tweets is not None:
            while tweets:
                tweet_item = tweets.pop()
                tweet(oauth,tweet_item)
        time.sleep(300) #5 minutes

