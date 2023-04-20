import functools

import requests
from urllib.parse import quote_plus


# ALWAYS USE QUOTE_PLUS, quote encodes ' ' as '%20', not as '+'
url_encode = functools.partial(quote_plus, safe='')


class APIaccess(object):

    def __init__(self, api_key):
        self._API_KEY = api_key
        self.configs = self.get_configs()
        # print(self.configs)

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
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

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
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_movie_details(self, movie_id):
        try:
            params = {
                'api_key': self._API_KEY
            }
            result = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "?", params)
            if result.status_code == 200:
                # with open("details_ex.json", "w") as w:
                #     w.write(json.dumps(result.json()))
                return result.json()
            else:
                raise Exception("Error while fetching movie details, response status code:", result.status_code)
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_similar_movies(self, movie_id):
        try:
            params = {
                'api_key': self._API_KEY
            }
            result = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "/similar", params)
            if result.status_code == 200:
                return result.json().get('results')
            else:
                raise Exception("Error while fetching movie details, response status code:", result.status_code)
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_recommendations(self, movie_id):
        try:
            params = {
                'api_key': self._API_KEY
            }
            result = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "/recommendations", params)
            if result.status_code == 200:
                return result.json().get('results')
            else:
                raise Exception("Error while fetching movie details, response status code:", result.status_code)
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_popular_movies(self):
        try:
            params = {
                'api_key': self._API_KEY
            }
            result = requests.get("https://api.themoviedb.org/3/movie/popular",
                                  params)
            if result.status_code == 200:
                return result.json().get('results')
            else:
                raise Exception("Error while fetching movie details, response status code:", result.status_code)
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_upcoming_movies(self):
        try:
            params = {
                'api_key': self._API_KEY
            }
            result = requests.get("https://api.themoviedb.org/3/movie/upcoming",
                                  params)
            if result.status_code == 200:
                return result.json().get('results')
            else:
                raise Exception("Error while fetching movie details, response status code:", result.status_code)
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_top_rated_movies(self, pages):
        try:
            movies = []
            for page in range(pages):
                params = {
                    'api_key': self._API_KEY,
                    'page': 1 + page
                }
                result = requests.get("https://api.themoviedb.org/3/movie/top_rated", params)
                if result.status_code == 200:
                    movies.extend(result.json().get('results'))
                else:
                    raise Exception("Error while fetching movie details, response status code:", result.status_code)
            print(movies)
            return movies
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def fetch_actors(self, movie_id):
        try:
            params = {
                'api_key': self._API_KEY
            }
            result = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits", params)
            if result.status_code == 200:
                return [actor for actor in result.json().get('cast')]
            else:
                raise Exception("Error while fetching movie details, response status code:", result.status_code)
        except Exception as err:
            print(f'Error occurred: {err}')
            return None
