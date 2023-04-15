from abc import ABC, abstractmethod
from tkinter import *
import customtkinter
import urllib3
import requests
from urllib3.exceptions import HTTPError
from PIL import Image
from models.User import User

configs = {}
API_KEY = '352322dd49f426559fac64881f6ecbb9'


class SearchParams(object):
    def __init__(self):
        self.title = ''


# TODO: export pages into seperate file(s?)
class Page(ABC):
    @staticmethod
    @abstractmethod
    def get_page_title():
        pass

    @staticmethod
    @abstractmethod
    def get_page_size():
        pass


class LoginPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager Login"

    @staticmethod
    def get_page_size():
        return "600x580"

    def __init__(self, master: customtkinter.CTkFrame, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.logo = customtkinter.CTkImage(
            # TODO: paths should not be windows hardcoded, use pathlib
            light_image=Image.open("src\\assets\\icon_1.png"),
            dark_image=Image.open("src\\assets\\icon_2.png"),
            size=(200, 200)
        )

        self.lbl_logo = customtkinter.CTkLabel(master=self, image=self.logo, text="", corner_radius=25)
        self.lbl_logo.pack(anchor="center", pady=(50, 10), padx=30)

        self.lbl_username = customtkinter.CTkLabel(master=self, text="Username")
        self.lbl_username.pack(anchor="center", pady=(25, 0), padx=30)
        self.username = StringVar()
        self.ent_username = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Username")
        self.ent_username.pack(anchor="center", pady=10, padx=30)

        self.lbl_password = customtkinter.CTkLabel(master=self, text="Password")
        self.lbl_password.pack(anchor="center", pady=0, padx=30)
        self.password = StringVar()
        self.ent_password = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password", show="•")
        self.ent_password.pack(anchor="center", pady=10, padx=30)

        self.frm_buttons = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.frm_buttons.grid_rowconfigure(0, weight=1)  # configure grid system
        self.frm_buttons.grid_columnconfigure(0, weight=1)
        self.frm_buttons.grid_columnconfigure(1, weight=1)
        self.frm_buttons.login_button = customtkinter.CTkButton(
            master=self.frm_buttons,
            width=200,
            height=40,
            corner_radius=20,
            text="Log In",
            command=controller.login_user
        )
        self.frm_buttons.login_button.grid(row=0, column=0, pady=5, padx=10)
        self.frm_buttons.register_button = customtkinter.CTkButton(
            master=self.frm_buttons,
            width=200,
            height=40,
            corner_radius=20,
            text="Register",
            command=lambda: controller.show_frame(RegisterPage)
        )
        self.frm_buttons.register_button.grid(row=0, column=1, pady=5, padx=10)
        self.frm_buttons.pack(anchor="center", pady=(25, 50), padx=20)


class RegisterPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager Register"

    @staticmethod
    def get_page_size():
        return "600x740"

    def __init__(self, master: customtkinter.CTkFrame, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.logo = customtkinter.CTkImage(
            light_image=Image.open("src\\assets\\icon_1.png"),
            dark_image=Image.open("src\\assets\\icon_2.png"),
            size=(200, 200)
        )

        self.lbl_logo = customtkinter.CTkLabel(master=self, image=self.logo, text="", corner_radius=25)
        self.lbl_logo.pack(anchor="center", pady=(50, 10), padx=30)

        self.lbl_username = customtkinter.CTkLabel(master=self, text="Username")
        self.lbl_username.pack(anchor="center", pady=(25, 0), padx=30)
        self.username = StringVar()
        self.ent_username = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="the_Dude", textvariable=self.username)
        self.ent_username.pack(anchor="center", pady=10, padx=30)

        self.lbl_email = customtkinter.CTkLabel(master=self, text="E-mail Address")
        self.lbl_email.pack(anchor="center", pady=0, padx=30)
        self.email = StringVar()
        self.ent_email = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="big_lebowski@gmail.com", textvariable=self.email)
        self.ent_email.pack(anchor="center", pady=10, padx=30)

        self.lbl_password = customtkinter.CTkLabel(master=self, text="Password")
        self.lbl_password.pack(anchor="center", pady=0, padx=30)
        self.password = StringVar()
        self.ent_password = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password", show="•", textvariable=self.password)
        self.ent_password.pack(anchor="center", pady=10, padx=30)

        self.lbl_password_again = customtkinter.CTkLabel(master=self, text="Password Confirmation")
        self.lbl_password_again.pack(anchor="center", pady=0, padx=30)
        self.password_again = StringVar()
        self.ent_password_again = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password Confirmation", show="•", textvariable=self.password_again)
        self.ent_password_again.pack(anchor="center", pady=10, padx=30)

        self.register_button = customtkinter.CTkButton(
            master=self,
            width=200,
            height=40,
            corner_radius=20,
            text="Register",
            command=lambda: controller.register_user(User(self.username, self.email, self.password, self.password_again))
        )
        self.register_button.pack(anchor="center", pady=(25, 50), padx=20)

        self.btn_back = customtkinter.CTkButton(
            master=self,
            height=30,
            corner_radius=15,
            text='Back',
            command=lambda: controller.show_frame(LoginPage),
            fg_color="#142d5e",
            text_color="#5584CC"
        )
        self.btn_back.place(anchor="nw", x=20, y=20)


# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")           # #2fa572
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
        for F in (LoginPage, RegisterPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)
        # self.center_window()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.title(cont.get_page_title())
        print(cont.get_page_size())
        self.geometry(cont.get_page_size())
        # self.center_window()

    def login_user(self):
        pass

    def register_user(self, user):
        pass

# https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
    def center_window(self, width, height):
        w = width
        h = height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))


def get_configs():
    global configs
    try:
        print('Fetching API configs.')
        configs = requests.get("https://api.themoviedb.org/3/configuration?", params={'api_key': API_KEY}).json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')


if __name__ in {"__main__", "__mp_main__"}:
    get_configs()
    app = App()

    # https://stackoverflow.com/a/9109106
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)

    app.mainloop()




# self.sp = SearchParams()
#
#         # self.grid_rowconfigure("all", weight=1)  # configure grid system
#         # self.grid_columnconfigure("all", weight=1)
#
#         self.search_title_label = customtkinter.CTkLabel(master=self, text="Movie title")
#         # self.search_title_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)
#         self.search_title_label.pack(anchor="center", expand=1)
#
#         self.search_title = StringVar()
#         self.search_title_entry = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="The Big Lebowski")
#         # self.search_title_entry.grid(row=1, column=0, sticky="we")
#         self.search_title_entry.pack(anchor="center")
#
#         self.search_button = customtkinter.CTkButton(master=self, width=200, corner_radius=10, text="Search", command=self.search)
#         # self.search_button.grid(row=1, column=1)
#         self.search_button.pack(anchor="center", expand=1)
#
#         self.withdraw()
