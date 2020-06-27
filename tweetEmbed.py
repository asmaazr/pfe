import requests


def embedTw(tweet_id):
    tweet_request = requests.get('https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/' +
                                 str(tweet_id)+'&hide_media=true'+'&hide_thread=true'+'&data-cards="hidden"')
    tweet_json = tweet_request.json()
    tweet_html = tweet_json['html']
    return tweet_html
