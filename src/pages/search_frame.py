import asyncio
import pathlib
import customtkinter
from PIL import Image

from src.pages.main_frame import MainFrame


class SearchFrame(MainFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)

        self.controller = controller

        self.seg_categories = customtkinter.CTkSegmentedButton(
            master=self,
            values=["Search", "Top Rated", "Popular", "Upcoming"],
            command=lambda e: self.categories_handler())
        self.seg_categories.pack(padx=20, pady=10)
        self.seg_categories.set("Search")  # set initial value

        self.lbl_page_title = customtkinter.CTkLabel(master=self, text="Search", font=('Roboto', 22, 'bold'))
        self.lbl_page_title.pack(pady=10)

        self.lbl_movie_title = customtkinter.CTkLabel(master=self, text="Search for a movie title!", width=500)
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

    def categories_handler(self):
        cat = self.seg_categories.get()
        if cat != "Search":
            self.controller.load_movies(t=cat.lower())
