from tkinter import *
import customtkinter
from models.User import User
from src.API import APIaccess
from src.pages.MainPage import MainPage
from src.pages.LoginPage import LoginPage
from src.pages.RegisterPage import RegisterPage


# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_page = None
        self.api = APIaccess('352322dd49f426559fac64881f6ecbb9')

        ###############################################################
        #                    API TEST ZONE                            #
        ###############################################################

        # print(self.api.fetch_movies("The Big Lebowski"))
        # print(self.api.fetch_movies("Cars"))
        # print(self.api.fetch_movies("Finding Nemo"))

        ###############################################################

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")  # #2fa572
        self.minsize(width=520, height=600)
        self.title("MovieManager")
        self.geometry("600x580")
        self.center_window(600, 580)
        # self.resizable(False, False)

        self.container = customtkinter.CTkFrame(self, height=480, width=720)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = dict()
        for F in (LoginPage, RegisterPage, MainPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.bind("<Return>", lambda e: self.handle_return())
        self.show_page("LoginPage")
        # self.center_window()

    def show_page(self, cont):
        self.current_page = cont;
        page = eval(cont)
        frame = self.frames[page]
        frame.tkraise()
        self.title(page.get_page_title())
        # print(page.get_page_size())
        self.geometry(page.get_page_size())
        self.center_window()

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
        l_p = self.frames[LoginPage]
        print("User login attempt:", l_p.ent_username.get())

        if l_p.ent_username.get() == 'letmein':
            print("legit.")
            self.show_page("MainPage")

        # TODO

    def register_user(self):
        r_p = self.frames[RegisterPage]
        print("User registering:")
        print(r_p.ent_username.get())
        print(r_p.ent_email.get())
        pw_match = r_p.ent_password.get() != r_p.ent_password_again.get()
        print("Passwords", "" if pw_match else "don't", "match.")
        # TODO

    def handle_return(self):
        if self.current_page == "RegisterPage":
            self.register_user()
        elif self.current_page == "LoginPage":
            self.register_user()
        elif self.current_page == "MainPage":
            print("🤡")
            # todo?


if __name__ in {"__main__", "__mp_main__"}:
    app = App()

    # https://stackoverflow.com/a/9109106 - starting minimized fix
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)

    app.mainloop()
