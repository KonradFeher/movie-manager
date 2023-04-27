# Model for user
class User(object):
    def __init__(self, username, email, watched_ids=None, watchlist_ids=None):
        if watchlist_ids is None:
            watchlist_ids = []
        if watched_ids is None:
            watched_ids = []
        self.username = username
        self.email = email
        self.watched_ids = watched_ids
        self.watchlist_ids = watchlist_ids

    def __str__(self):
        return f'username: {self.username}, email: {self.email}, ' \
               f'watched_ids: {self.watched_ids}, watchlist_ids: {self.watchlist_ids}'
