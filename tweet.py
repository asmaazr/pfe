import tweepy
import re
# Salah's keys 
#access_token = "1030804524649340929-uYOzvbWSRXuo9OVjXS64jJZBlFXWDR"
#access_token_secret = "j5dunyBRvuLnrrUp4mtA0AMHLXqG4TId1aa29c3KVqjyx"
#consumer_key = "TwVQJ3LVVmQTqn8XQ1kc9hmJU"
#consumer_secret = "sLDWNIo22ZMwBVXiTPtdrR8RnSzvOlNKYyHglLkPsl4sgBRkuj"
# my keys 
access_token = "4866943671-qlYHiPZHZ01Y6ixV19ygXwTTpwlhCstREQ0QIzq"
access_token_secret = "WOQp1CB5piggvG1DoJtQXelIZPi8YmJedBNukF1hgswKD"
consumer_key = "ZluaQUfhoG2d0TcnMCBbOsXrC"
consumer_secret = "9he49UFUBvTka49UpzN54SEoTLhwMCQi3XeNULcoxapeKHupDr"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def stream_tweets(search_terms):
    data = [] # empty list to which tweet_details obj will be added
    for search_term in search_terms:
        search_term = search_term.replace("_", " ")
        for tweet in tweepy.Cursor(api.search, q='{} -filter:retweets AND -filter:replies'.format(search_term) , lang='en', tweet_mode='extended', result_type='mixed').items(100):
            tweet_details = {}
            if  (str(tweet.user.verified).lower() == 'true') or (str(tweet.user.screen_name).lower() == str(search_term).lower()):
              continue
            else:
                tweet_details['id_tweet'] = tweet.id_str
                tweet_details['airline'] = search_term
                tweet_details['name'] = tweet.user.screen_name
                tweet_details['tweet'] = re.sub(r"http\S+", "", tweet.full_text)
                tweet_details['created'] = tweet.created_at.strftime("%d/%m/%Y, %H:%M:%S")
                tweet_details['location'] = tweet.user.location
                tweet_details['followers'] = tweet.user.followers_count
                tweet_details['is_user_verified'] = tweet.user.verified        
                data.append(tweet_details)
        
    return data

