import asyncio
import pathlib

import customtkinter
from PIL import Image


class WatchlistFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.default_poster = Image.open(pathlib.Path("assets", "icon.png"))
        self.controller = controller
        self.result_columns = 3
        self.lbl_movie_title = customtkinter.CTkLabel(master=self, text="Watchlist", width=500)
        self.lbl_movie_title.pack(pady=(20, 5))
        self.ent_movie_title = customtkinter.CTkEntry(master=self, width=400, corner_radius=5,
                                                      placeholder_text="The Big Lebowski", border_width=3)
        self.ent_movie_title.pack()

        self.btn_search = customtkinter.CTkButton(
            master=self,
            width=200,
            height=40,
            corner_radius=20,
            text="Search",
            command=lambda: controller.search_movies(self.ent_movie_title.get())
        )
        self.btn_search.pack(pady=(20, 20))
