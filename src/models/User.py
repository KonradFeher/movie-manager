class User(object):
    def __init__(self, username, email, password, password_again):
        self.username = username
        self.email = email
        self.password = password
        self.password_again = password_again
        # this is temporary, controller should verify the entries first, then deal with the model
