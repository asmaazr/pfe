import wikipedia
import requests
import json
def wikipd(search_term):
    sumr = wikipedia.summary(search_term)[0:300]
    return sumr
def get_image(search_term):
    wikipage = wikipedia.page(search_term)
    return  wikipage.images[0]



WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0


    



  