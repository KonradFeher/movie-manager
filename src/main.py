import re
from io import BytesIO
from tkinter import *
from PIL import Image
import customtkinter
import requests
from src.API import APIaccess
from src.Database import Database
from src.pages.MainPage import MainPage
from src.pages.LoginPage import LoginPage
from src.pages.RegisterPage import RegisterPage
import difflib

# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
from src.pages.SearchFrame import SearchFrame


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_page = None
        self.active_user = None
        self.api = APIaccess('352322dd49f426559fac64881f6ecbb9')

        ###############################################################
        #                    API TEST ZONE                            #
        ###############################################################

        # print(self.api.fetch_movies("The Big Lebowski"))
        # print(self.api.fetch_movies("Cars"))
        # print(self.api.fetch_movies("Finding Nemo"))

        ###############################################################

        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("dark-blue")  # #2fa572
        self.minsize(width=520, height=600)
        self.title("MovieManager")
        self.geometry("600x580+300+100")
        # self.center_window(600, 580)
        # self.resizable(False, False)

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
        # self.center_window()

    def show_page(self, cont):
        self.focus_set()
        self.current_page = cont
        page = eval(cont)
        frame = self.pages[page]
        frame.tkraise()
        self.title(page.get_page_title())
        # print(page.get_page_min_size())
        minsize = page.get_page_min_size().split('x')
        self.minsize(width=int(minsize[0]), height=int(minsize[1]))
        if page.get_page_max_size() is not None:
            maxsize = page.get_page_max_size().split('x')
            self.maxsize(width=int(maxsize[0]), height=int(maxsize[1]))
        # print(page.get_page_size())
        self.geometry(page.get_page_size())
        # self.center_window()
        if page == MainPage:
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
        if username_or_email == 'letmein':
            self.show_page("MainPage")

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
                self.show_page('MainPage')
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
        if not re.fullmatch(r'[a-zA-Z0-9]{4,20}', username):
            errors.append("Username is invalid. \n 4-20 characters, a-z A-Z 0-9 are allowed.")
        if not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
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
        # print(self._current_width, self._current_height)
        # print(self.current_page)
        if self.current_page == "RegisterPage":
            self.register_user()
        elif self.current_page == "LoginPage":
            self.login_user()
        elif self.current_page == "MainPage":
            self.search_movies(self.pages[MainPage].frames[SearchFrame].ent_movie_title.get())

    def get_movie_poster(self, path, typ='poster', size=1):
        if path is not None and path != 0 and path != "":
            img_conf = self.api.configs.get('images')
            # print(img_conf.get('base_url') + img_conf.get(typ + '_sizes')[size] + path)
            response = requests.get(img_conf.get('base_url') + img_conf.get(typ + '_sizes')[size] + path)
            return Image.open(BytesIO(response.content))

    def search_movies(self, title):
        print("Searching for", title)
        search_frame = self.pages[MainPage].frames[SearchFrame]
        # m_p.progress_bar.grid(row=4, column=1, pady=(0, 30))
        # m_p.progress_bar.start()
        search_frame.clear_results()
        request_response = self.api.fetch_movies(title)
        # print(request_response)
        results = sorted(
            request_response.get('results'),
            key=lambda x: difflib.SequenceMatcher(a=x['title'].lower(), b=title.lower()).ratio() ** 2 * x['popularity'],
            reverse=True
        )
        for result in results:
            # print(result['title'], "-", result['popularity'] *
            #   difflib.SequenceMatcher(a=result['title'].lower(), b=title.lower()).ratio()**2)
            # self.update_idletasks()
            try:
                search_frame.add_result(result)
            except Exception as e:
                print("HUH?", e)
        search_frame.refresh_results()
        # m_p.progress_bar.stop()
        # m_p.progress_bar.grid_forget()


if __name__ in {"__main__", "__mp_main__"}:
    app = App()

    # https://stackoverflow.com/a/9109106 - starting minimized fix
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)

    app.mainloop()
