import functools

import requests
from urllib3.exceptions import HTTPError
from urllib.parse import quote_plus


# ALWAYS USE QUOTE_PLUS, quote encodes ' ' as '%20', not as '+'
url_encode = functools.partial(quote_plus, safe='')


class APIaccess(object):

    def __init__(self, api_key):
        self._API_KEY = api_key
        self.configs = self.get_configs()

    def get_configs(self):
        try:
            print('Fetching API configs.')
            result = requests.get("https://api.themoviedb.org/3/configuration?",
                                  params={
                                      'api_key': self._API_KEY
                                  })
            print('Request result: ', result.status_code)
            if result.status_code == 200:
                return result.json()
            else:
                raise Exception("Error while fetching configuration, response status code:", result.status_code)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def fetch_movies(self, query, page=1, year=None, include_adult=False):
        try:
            params = {
                'api_key': self._API_KEY,
                'language': 'en-US',
                'query': url_encode(query),
                'page': page,
                'include_adult': include_adult
            }
            if year:
                print("set year to", year)
                params['year'] = year
            result = requests.get("https://api.themoviedb.org/3/search/movie?", params)
            print(f'Fetching "{query}" ({year}) movies, page {page}...')
            print('Request result: ', result.status_code)
            if result.status_code == 200:
                return result.json()
            else:
                raise Exception("Error while fetching movies, response status code:", result.status_code)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')