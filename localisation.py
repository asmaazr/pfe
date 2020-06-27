import requests
import json

def get_loc(country):
    try:
        url = '{0}{1}{2}'.format(
            'http://nominatim.openstreetmap.org/search?country=', country, '&format=json&polygon=0')
        response = requests.get(url).json()[0]
        lst = [response.get(key) for key in ['lat', 'lon']]
        return [float(i) for i in lst]
    except IndexError:
        return