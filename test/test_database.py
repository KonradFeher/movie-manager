import os
import unittest
from unittest.mock import MagicMock

import bcrypt

from src.database import Database
from src.models.user import User


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database("test.db")
        self.db.create_tables()
        self.db.create_user("test_user", "test_user@example.com", "password")

    def tearDown(self):
        self.db.cur.execute("DROP TABLE users")
        self.db.cur.execute("DROP TABLE watched")
        self.db.cur.execute("DROP TABLE watchlist")
        self.db.con.close()
        os.remove('test.db')

    def test_fetch_user_by_email(self):
        user = self.db.fetch_user_by_email("test_user@example.com")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test_user@example.com")

    def test_create_user(self):
        created = self.db.create_user("test_user_2", "test_user_2@example.com", "password")
        self.assertTrue(created)
        user = self.db.fetch_user_by_email("test_user_2@example.com")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "test_user_2")
        self.assertEqual(user.email, "test_user_2@example.com")

        created = self.db.create_user("test_user_2", "test_user_2@example.com", "password")
        self.assertFalse(created)

    def test_fetch_watched_by_email(self):
        watched = self.db.fetch_watched_by_email("dummy_email@gmail.com")
        self.assertEqual(watched, [1, 3])

    def test_fetch_watchlist_by_email(self):
        watchlist = self.db.fetch_watchlist_by_email("dummy_email@gmail.com")
        self.assertEqual(watchlist, [5, 70, 29])

    def test_delete_from_watched(self):
        self.db.delete_from_watched("dummy_email@gmail.com", 1)
        watched = self.db.fetch_watched_by_email("dummy_email@gmail.com")
        self.assertEqual(watched, [3])

        self.db.delete_from_watched("dummy_email@gmail.com", 1)
        watched = self.db.fetch_watched_by_email("dummy_email@gmail.com")
        self.assertEqual(watched, [3])

    def test_delete_from_watchlist(self):
        self.db.delete_from_watchlist("dummy_email@gmail.com", 5)
        watchlist = self.db.fetch_watchlist_by_email("dummy_email@gmail.com")
        self.assertEqual(watchlist, [70, 29])

        self.db.delete_from_watchlist("dummy_email@gmail.com", 5)
        watchlist = self.db.fetch_watchlist_by_email("dummy_email@gmail.com")
        self.assertEqual(watchlist, [70, 29])

    def test_add_to_watched(self):
        added = self.db.add_to_watched("dummy_email@gmail.com", 2)
        self.assertTrue(added)
        watched = self.db.fetch_watched_by_email("dummy_email@gmail.com")
        self.assertEqual(watched, [1, 3, 2])

        added = self.db.add_to_watched("dummy_email@gmail.com", 1)
        self.assertFalse(added)
        watched = self.db.fetch_watched_by_email("dummy_email@gmail.com")
        self.assertEqual(watched, [1, 3, 2])

    def test_add_to_watchlist(self):
        added = self.db.add_to_watchlist("dummy_email@gmail.com", 10)
        self.assertTrue(added)
        watchlist = self.db.fetch_watchlist_by_email("dummy_email@gmail.com")
        self.assertEqual(watchlist, [5, 70, 29, 10])

        added = self.db.add_to_watchlist("dummy_email@gmail.com", 5)
        self.assertFalse(added)

    def test_verify_credentials_incorrect(self):
        db = Database()
        db.cur = MagicMock()
        db.cur.fetchall.return_value = []
        user = db.verify_credentials('testuser', 'testpassword')
        self.assertFalse(user)

    def test_user_exists_email(self):
        db = Database()
        db.cur = MagicMock()
        db.cur.fetchall.return_value = [('testuser', 'testemail@test.com', bcrypt.hashpw(b'testpassword', bcrypt.gensalt()))]
        exists = db.user_exists(email='testemail@test.com')
        self.assertTrue(exists)

    def test_user_exists_username(self):
        db = Database()
        db.cur = MagicMock()
        db.cur.fetchall.return_value = [('testuser', 'testemail@test.com', bcrypt.hashpw(b'testpassword', bcrypt.gensalt()))]
        exists = db.user_exists(username='testuser')
        self.assertTrue(exists)

    def test_user_exists_no_inputs(self):
        db = Database()
        exists = db.user_exists()
        self.assertTrue(exists)

    def test_user_exists_not_found(self):
        db = Database()
        db.cur = MagicMock()
        db.cur.fetchall.return_value = []
        exists = db.user_exists(username='testuser')
        self.assertFalse(exists)