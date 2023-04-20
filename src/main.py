import re
from io import BytesIO
from PIL import Image
import customtkinter
import requests
from src.API import APIaccess
from src.Database import Database
from src.pages.MainPage import MainPage
from src.pages.LoginPage import LoginPage
from src.pages.MovieFrame import MovieFrame
from src.pages.RegisterPage import RegisterPage
import difflib

# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
from src.pages.SearchFrame import SearchFrame
from src.pages.WatchedFrame import WatchedFrame
from src.pages.WatchlistFrame import WatchlistFrame


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_page = None
        self.active_user = None
        self.api = APIaccess('352322dd49f426559fac64881f6ecbb9')
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("dark-blue")  # #2fa572
        self.minsize(width=520, height=600)
        self.title("MovieManager")
        self.geometry("600x580+300+100")

        self.container = customtkinter.CTkFrame(self, height=480, width=720)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = dict()
        for F in (LoginPage, RegisterPage, MainPage):
            frame = F(self.container, self)
            self.pages[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.bind("<Return>", lambda e: self.handle_return())

        self.show_page("LoginPage")
        self.current_page = "LoginPage"

    def show_page(self, cont, first=False):
        self.focus_set()
        self.current_page = cont
        page = eval(cont)
        frame = self.pages[page]
        frame.tkraise()
        self.title(page.get_page_title())
        minsize = page.get_page_min_size().split('x')
        self.minsize(width=int(minsize[0]), height=int(minsize[1]))
        if page.get_page_max_size() is not None:
            maxsize = page.get_page_max_size().split('x')
            self.maxsize(width=int(maxsize[0]), height=int(maxsize[1]))
        self.geometry(page.get_page_size())
        if page == MainPage and first:
            self.search_movies("The Big Lebowski")

    # https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
    def center_window(self, width=1, height=1):
        w = self._current_width
        h = self._current_height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def login_user(self):
        login_page = self.pages[LoginPage]

        username_or_email = login_page.ent_username_or_email.get()
        password = login_page.ent_password.get()

        print("User login attempt:", username_or_email)
        # backdoor
        # if username_or_email == 'letmein':
        #     self.show_page("MainPage")

        # if either of the fields is empty, stop login attempt
        if len(username_or_email) == 0 or len(password) == 0:
            login_page.display_incorrect()
            return False

        with Database("movie-manager.db") as db:
            user = db.verify_credentials(username_or_email, password)
            if user:
                login_page.display_incorrect(show=False)
                self.active_user = user
                print("Successful login")
                self.show_page('MainPage', first=True)
                return
            else:
                print("Unsuccessful login")
                login_page.display_incorrect()
                return

    def register_user(self):
        register_page = self.pages[RegisterPage]

        email = register_page.ent_email.get()
        username = register_page.ent_username.get()
        password = register_page.ent_password.get()
        password_2 = register_page.ent_password_again.get()
        print("User registering:")
        print(username)
        print(email)

        errors = []
        if not re.fullmatch(r'[a-zA-Z\d]{4,20}', username):
            errors.append("Username is invalid. \n 4-20 characters, a-z A-Z 0-9 are allowed.")
        if not re.fullmatch(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+', email):
            errors.append("Email is invalid.")
        if len(password) < 6:
            errors.append("Password too short. (6-64)")
        if len(password) > 64:
            errors.append("Password too long. (6-64)")
        if password != password_2:
            errors.append("Passwords don't match.")

        with Database("movie-manager.db") as db:
            if db.user_exists(username=username):
                errors.append("User already exists with that username.")
            if db.user_exists(email=email):
                errors.append("User already exists with that email address.")
            register_page.display_errors(errors)
            if len(errors) > 0:
                print("Register unsuccessful.")
                return
            db.create_user(username, email, password)
            print("Register successful.")
            self.show_page('LoginPage')

    def handle_return(self):
        if self.current_page == "RegisterPage":
            self.register_user()
        elif self.current_page == "LoginPage":
            self.login_user()
        elif self.current_page == "MainPage":
            self.search_movies(self.pages[MainPage].frames[SearchFrame].ent_movie_title.get())

    def get_movie_image(self, path, typ='poster', size=1):
        if path is not None and path != 0 and path != "":
            img_conf = self.api.configs.get('images')
            response = requests.get(img_conf.get('base_url') + img_conf.get(typ + '_sizes')[size] + path)
            return Image.open(BytesIO(response.content))
        else:
            return None

    def search_movies(self, title):
        print("Searching for", title)
        search_frame = self.pages[MainPage].frames[SearchFrame]
        search_frame.seg_categories.set("Search")
        search_frame.reset_results_frame()
        request_response = self.api.fetch_movies(title)
        results = sorted(
            request_response.get('results'),
            key=lambda x: difflib.SequenceMatcher(a=x['title'].lower(), b=title.lower()).ratio() ** 2 * x['popularity'],
            reverse=True
        )
        for result in results:
            try:
                search_frame.add_result(result)
            except Exception as e:
                print("HUH?", e)
        search_frame.refresh_results()

    def show_movie(self, movie):
        movie_details = self.api.fetch_movie_details(movie.get('id'))
        movie_actors = self.api.fetch_actors(movie.get('id'))
        self.pages[MainPage].frames[MovieFrame].load_movie(movie_details, movie_actors)
        self.pages[MainPage].show_frame('MovieFrame')

    def add_to_watchlist(self, movie):
        self.pages[MainPage].frames[MovieFrame].btn_watchlist.configure(state="disabled")
        self.pages[MainPage].frames[MovieFrame].btn_watched_it.configure(state="normal")
        with Database("movie-manager.db") as db:
            db.add_to_watchlist(self.active_user.email, movie.get('id'))
            self.active_user.watchlist_ids.append(movie.get('id'))

    def add_to_watched(self, movie):
        self.pages[MainPage].frames[MovieFrame].btn_watched_it.configure(state="disabled")
        self.pages[MainPage].frames[MovieFrame].btn_watchlist.configure(state="normal")
        with Database("movie-manager.db") as db:
            db.add_to_watched(self.active_user.email, movie.get('id'))
            self.active_user.watched_ids.append(movie.get('id'))

    def go_to_watched(self):
        self.pages[MainPage].frames[WatchedFrame].reset_results_frame()
        with Database("movie-manager.db") as db:
            watched_ids = db.fetch_watched_by_email(self.active_user.email)
            # print(watched_ids)
            watched_ids.reverse()
        for wid in watched_ids:
            movie = self.api.fetch_movie_details(wid)
            self.pages[MainPage].frames[WatchedFrame].add_result(movie)
        self.pages[MainPage].frames[WatchedFrame].refresh_results()
        self.pages[MainPage].show_frame("WatchedFrame")

    def go_to_watchlist(self):
        self.pages[MainPage].frames[WatchlistFrame].reset_results_frame()
        with Database("movie-manager.db") as db:
            watchlist_ids = db.fetch_watchlist_by_email(self.active_user.email)
            print(watchlist_ids)
            watchlist_ids.reverse()
        for wid in watchlist_ids:
            movie = self.api.fetch_movie_details(wid)
            self.pages[MainPage].frames[WatchlistFrame].add_result(movie)
        self.pages[MainPage].frames[WatchlistFrame].refresh_results()
        self.pages[MainPage].show_frame("WatchlistFrame")

    def load_movies(self, movie=None, t="recommendations"):
        if movie is None:
            movie = {'id': 115}
        search_frame = self.pages[MainPage].frames[SearchFrame]
        search_frame.reset_results_frame()
        results = None
        t = t.lower()
        print(t)
        if t == "recommendations":
            results = self.api.fetch_recommendations(movie.get('id'))
        if t == "similar":
            results = self.api.fetch_similar_movies(movie.get('id'))
        if t == "top rated":
            results = self.api.fetch_top_rated_movies(pages=3)
        if t == "popular":
            results = self.api.fetch_popular_movies()
        if t == "upcoming":
            results = self.api.fetch_upcoming_movies()

        print('results:', results)

        for result in results:
            try:
                search_frame.add_result(result)
            except Exception as e:
                print("HUH???", e)
        search_frame.refresh_results()
        self.show_page('MainPage')
        self.pages[MainPage].show_frame('SearchFrame')


if __name__ in {"__main__", "__mp_main__"}:
    app = App()

    # https://stackoverflow.com/a/9109106 - starting minimized fix
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)

    app.mainloop()
