from src.models.user import User


def test_user_creation():
    user = User('testuser', 'testemail@example.com')
    assert user.username == 'testuser'
    assert user.email == 'testemail@example.com'
    assert user.watched_ids == []
    assert user.watchlist_ids == []


def test_user_creation_with_watched_ids():
    user = User('testuser', 'testemail@example.com', watched_ids=[1, 2, 3])
    assert user.username == 'testuser'
    assert user.email == 'testemail@example.com'
    assert user.watched_ids == [1, 2, 3]
    assert user.watchlist_ids == []


def test_user_creation_with_watchlist_ids():
    user = User('testuser', 'testemail@example.com', watchlist_ids=[4, 5, 6])
    assert user.username == 'testuser'
    assert user.email == 'testemail@example.com'
    assert user.watched_ids == []
    assert user.watchlist_ids == [4, 5, 6]


def test_user_creation_with_watched_and_watchlist_ids():
    user = User('testuser', 'testemail@example.com', watched_ids=[1, 2, 3], watchlist_ids=[4, 5, 6])
    assert user.username == 'testuser'
    assert user.email == 'testemail@example.com'
    assert user.watched_ids == [1, 2, 3]
    assert user.watchlist_ids == [4, 5, 6]


def test_user_str_representation():
    user = User('testuser', 'testemail@example.com', watched_ids=[1, 2, 3], watchlist_ids=[4, 5, 6])
    assert str(user) == 'username: testuser, email: testemail@example.com, watched_ids: [1, 2, 3], watchlist_ids: [4, 5, 6]'
