import tweepy
import re
import pycountry
# Salah's keys
access_token = "1030804524649340929-t7QLsP6e6eiepAJxGnGymG672JhzIs"
access_token_secret = "J9DPtE4RmQRYoHh4NtDh0I89fxy0L25nvr63oFeg1CGhI"
consumer_key = "dX4kqtp4hes4f2jz5lNd7st1L"
consumer_secret = "vOe8sPhhYpbSRcZMONGjzjVxauljZlvaHujWAu4Piq5YbkTVK2"
# my keys
#access_token = "4866943671-qlYHiPZHZ01Y6ixV19ygXwTTpwlhCstREQ0QIzq"
#access_token_secret = "WOQp1CB5piggvG1DoJtQXelIZPi8YmJedBNukF1hgswKD"
#consumer_key = "ZluaQUfhoG2d0TcnMCBbOsXrC"
#consumer_secret = "9he49UFUBvTka49UpzN54SEoTLhwMCQi3XeNULcoxapeKHupDr"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def stream_tweets(search_terms):
    data = []  # empty list to which tweet_details obj will be added
    for search_term in search_terms:
        search_term = search_term.replace("_", " ")
        for tweet in tweepy.Cursor(api.search, q='{} -filter:retweets AND -filter:replies'.format(search_term), lang='en', tweet_mode='extended', result_type='mixed').items(200):
            tweet_details = {}
            if (str(tweet.user.verified).lower() == 'true') or (str(tweet.user.screen_name).lower() == str(search_term).lower()):
              continue
            else:
                tweet_details['id_tweet'] = tweet.id_str
                tweet_details['airline'] = search_term
                tweet_details['name'] = tweet.user.screen_name
                tweet_details['tweet'] = re.sub(
                    r"http\S+", "", tweet.full_text)
                tweet_details['created'] = tweet.created_at.strftime(
                    "%d/%m/%Y, %H:%M:%S")
                tweet_details['location'] = tweet.user.location
                tweet_details['followers'] = tweet.user.followers_count
                tweet_details['is_user_verified'] = tweet.user.verified
                for country in pycountry.countries:
                    if country.name in tweet.user.location:
                      tweet_details['location'] = country.name
                data.append(tweet_details)

    return data