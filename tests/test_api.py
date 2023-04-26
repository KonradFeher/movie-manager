import unittest
from unittest.mock import patch

from src.API import APIaccess


class TestAPIaccess(unittest.TestCase):

    def setUp(self):
        self.api_key = "352322dd49f426559fac64881f6ecbb9"
        self.api = APIaccess(self.api_key)

    def test_get_configs(self):
        configs = self.api.get_configs()
        self.assertIsNotNone(configs)

    def test_fetch_movies(self):
        movies = self.api.fetch_movies("The Shawshank Redemption")
        self.assertIsNotNone(movies)
        self.assertIsInstance(movies, dict)
        self.assertIn('results', movies)

    def test_fetch_movie_details(self):
        movie_id = 278
        details = self.api.fetch_movie_details(movie_id)
        self.assertIsNotNone(details)
        self.assertIsInstance(details, dict)
        self.assertEqual(details['id'], movie_id)

    def test_fetch_similar_movies(self):
        movie_id = 278
        similar_movies = self.api.fetch_similar_movies(movie_id)
        self.assertIsNotNone(similar_movies)
        self.assertIsInstance(similar_movies, list)

    def test_fetch_recommendations(self):
        movie_id = 278
        recommendations = self.api.fetch_recommendations(movie_id)
        self.assertIsNotNone(recommendations)
        self.assertIsInstance(recommendations, list)

    def test_fetch_popular_movies(self):
        popular_movies = self.api.fetch_popular_movies()
        self.assertIsNotNone(popular_movies)
        self.assertIsInstance(popular_movies, list)

    def test_fetch_upcoming_movies(self):
        upcoming_movies = self.api.fetch_upcoming_movies()
        self.assertIsNotNone(upcoming_movies)
        self.assertIsInstance(upcoming_movies, list)

    def test_fetch_top_rated_movies(self):
        pages = 2
        top_rated_movies = self.api.fetch_top_rated_movies(pages)
        self.assertIsNotNone(top_rated_movies)
        self.assertIsInstance(top_rated_movies, list)

    @patch('src.API.requests.get')
    def test_get_configs_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        configs = access.get_configs()
        self.assertIsNone(configs)

    @patch('src.API.requests.get')
    def test_fetch_movies_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        movies = access.fetch_movies('query', page=1, year=None, include_adult=False)
        self.assertIsNone(movies)

    @patch('src.API.requests.get')
    def test_fetch_movie_details_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        movie_details = access.fetch_movie_details(12345)
        self.assertIsNone(movie_details)

    @patch('src.API.requests.get')
    def test_fetch_similar_movies_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        similar_movies = access.fetch_similar_movies(12345)
        self.assertIsNone(similar_movies)

    @patch('src.API.requests.get')
    def test_fetch_recommendations_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        recommendations = access.fetch_recommendations(12345)
        self.assertIsNone(recommendations)

    @patch('src.API.requests.get')
    def test_fetch_popular_movies_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        popular_movies = access.fetch_popular_movies()
        self.assertIsNone(popular_movies)

    @patch('src.API.requests.get')
    def test_fetch_upcoming_movies_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        upcoming_movies = access.fetch_upcoming_movies()
        self.assertIsNone(upcoming_movies)

    @patch('src.API.requests.get')
    def test_fetch_top_rated_movies_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        top_rated_movies = access.fetch_top_rated_movies(2)
        self.assertIsNone(top_rated_movies)

    @patch('src.API.requests.get')
    def test_fetch_actors_404(self, mock_get):
        mock_get.return_value.status_code = 404
        access = APIaccess('API_KEY')
        actors = access.fetch_actors(12345)
        self.assertIsNone(actors)
