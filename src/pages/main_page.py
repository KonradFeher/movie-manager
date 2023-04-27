import pathlib
import random
import customtkinter
from PIL import Image
import tkinter

from .movie_frame import MovieFrame
from .page import Page
from .search_frame import SearchFrame
from .watched_frame import WatchedFrame
from .watchlist_frame import WatchlistFrame


# consists of a navbar and a container frame, holds instances of  frame modules
class MainPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager"

    @staticmethod
    def get_page_size():
        return "920x740"

    @staticmethod
    def get_page_min_size():
        return "920x740"

    @staticmethod
    def get_page_max_size():
        return "920x1080"

    def __init__(self, master: customtkinter.CTkFrame, controller, **kwargs):
        super().__init__(master, **kwargs)
        # self.default_poster = Image.open(pathlib.Path("assets", "default_poster.jpg"))
        self.current_frame = "SearchFrame"
        self.controller = controller

        # side nav
        self.frm_nav = customtkinter.CTkFrame(master=self, corner_radius=0, width=150)
        self.frm_nav.pack(side=tkinter.LEFT, fill='both', expand=False)

        self.logo = customtkinter.CTkImage(
            light_image=Image.open(pathlib.Path("assets", "icon_1.png")),
            dark_image=Image.open(pathlib.Path("assets", "icon_2.png")),
            size=(125, 125)
        )

        def enter(label):
            label.configure(fg_color="#666")

        def leave(label):
            label.configure(fg_color="transparent")

        self.lbl_nav_logo = customtkinter.CTkLabel(master=self.frm_nav, text='', image=self.logo, width=125, height=125)
        self.lbl_nav_logo.pack()

        self.lbl_greeting = customtkinter.CTkLabel(master=self.frm_nav, text='Greetings!')
        self.lbl_greeting.pack()

        self.btn_logout = customtkinter.CTkButton(master=self.frm_nav, text='Log Out', command=controller.log_user_out)
        self.btn_logout.pack(pady=(5, 15))

        self.font = customtkinter.CTkFont(family="Prompt", size=18)

        self.frm_nav_search = customtkinter.CTkFrame(master=self.frm_nav, height=100, width=200,
                                                     corner_radius=5, fg_color=self.frm_nav.cget("fg_color"))
        self.frm_nav_search.pack(pady=5, padx=5)
        self.lbl_nav_search = customtkinter.CTkLabel(master=self.frm_nav_search, text='SEARCH', font=self.font)
        self.lbl_nav_search.pack(side=tkinter.LEFT)
        self.lbl_nav_search.bind("<Enter>", lambda e: enter(self.lbl_nav_search))
        self.lbl_nav_search.bind("<Leave>", lambda e: leave(self.lbl_nav_search))

        self.lbl_nav_search.bind("<Button-1>", lambda e: self.show_frame("SearchFrame"))
        self.frm_nav_search.bind("<Button-1>", lambda e: self.show_frame("SearchFrame"))

        self.frm_nav_watchlist = customtkinter.CTkFrame(master=self.frm_nav, height=100, width=200,
                                                        corner_radius=5, fg_color=self.frm_nav.cget("fg_color"))
        self.frm_nav_watchlist.pack(pady=5, padx=5)
        self.lbl_nav_watchlist = customtkinter.CTkLabel(master=self.frm_nav_watchlist, text='WATCHLIST', font=self.font)
        self.lbl_nav_watchlist.pack(side=tkinter.LEFT)
        self.lbl_nav_watchlist.bind("<Enter>", lambda e: enter(self.lbl_nav_watchlist))
        self.lbl_nav_watchlist.bind("<Leave>", lambda e: leave(self.lbl_nav_watchlist))

        self.lbl_nav_watchlist.bind("<Button-1>", lambda e: controller.go_to_watchlist())
        self.frm_nav_watchlist.bind("<Button-1>", lambda e: controller.go_to_watchlist())

        self.frm_nav_watched = customtkinter.CTkFrame(master=self.frm_nav, height=100, width=200,
                                                      corner_radius=5, fg_color=self.frm_nav.cget("fg_color"))
        self.frm_nav_watched.pack(pady=5, padx=5)
        self.lbl_nav_watched = customtkinter.CTkLabel(master=self.frm_nav_watched, text='WATCHED', font=self.font)
        self.lbl_nav_watched.pack(side=tkinter.LEFT)
        self.lbl_nav_watched.bind("<Enter>", lambda e: enter(self.lbl_nav_watched))
        self.lbl_nav_watched.bind("<Leave>", lambda e: leave(self.lbl_nav_watched))

        self.lbl_nav_watched.bind("<Button-1>", lambda e: controller.go_to_watched())
        self.frm_nav_watched.bind("<Button-1>", lambda e: controller.go_to_watched())

        # holds all frames that are on the right side of this page
        self.frames = dict()

        self.frame_container = customtkinter.CTkFrame(master=self)
        self.frame_container.pack(side=tkinter.RIGHT, fill='both', expand=True)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        for Frame in [SearchFrame, WatchedFrame, WatchlistFrame, MovieFrame]:
            frame = Frame(self.frame_container, self.controller)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame("SearchFrame")

    # brings frame to top
    def show_frame(self, param):
        self.focus_set()
        self.current_frame = param
        frame_class = eval(param)
        frame = self.frames[frame_class]
        frame.tkraise()

    # sets greeting on navbar
    def set_greeting(self, username):
        if username is None:
            self.lbl_greeting.configure(text='Greetings!')
        greetings = ['Hi,\n', 'Hello,\n', 'Welcome,\n', 'Greetings,\n']
        self.lbl_greeting.configure(text=random.choice(greetings) + username)
