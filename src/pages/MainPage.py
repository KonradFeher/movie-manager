import json
import pathlib

import customtkinter
from PIL import Image

from src.models.User import User
from src.pages.Page import Page
import asyncio


class MainPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager"

    @staticmethod
    def get_page_size():
        return "920x740"

    @staticmethod
    def get_page_min_size():
        return "10x10"

    def __init__(self, master: customtkinter.CTkFrame, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.default_poster = Image.open(pathlib.Path("assets", "default_poster.jpg"))
        self.parent = controller
        self.configure(border_width=3)
        self.result_columns = 3
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure('all', weight=1)

        self.lbl_movie_title = customtkinter.CTkLabel(master=self, text="Search for a movie title!", width=500)
        self.lbl_movie_title.grid(row=1, column=1, pady=(50, 5))
        self.ent_movie_title = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="The Big Lebowski", border_width=3)
        self.ent_movie_title.grid(row=2, column=1)

        self.btn_search = customtkinter.CTkButton(
            master=self,
            width=200,
            height=40,
            corner_radius=20,
            text="Search",
            command=lambda: controller.search_movies(self.ent_movie_title.get())
        )
        self.btn_search.grid(row=3, column=1, pady=(50, 50))

        self.frm_results = customtkinter.CTkScrollableFrame(master=self, height=450)
        self.frm_results.grid_rowconfigure("all", weight=1)
        for i in range(self.result_columns):
            self.frm_results.grid_columnconfigure(i,  weight=1)
        self.frm_results.grid(row=4, column=1, sticky="SNWE", padx=20)
        self.results = list()

    def add_result(self, movie):
        self.results.append(movie)

    def clear_results(self):
        self.results = list()

    def refresh_results(self):
        for widget in self.frm_results.winfo_children():
            widget.destroy()
        count = 0
        # with open("example_result.json", "w") as w:
        #     w.write(json.dumps(self.results))
        for movie in self.results:
            frm_movie_card = customtkinter.CTkFrame(master=self.frm_results, width=150, height=300)

            lbl_movie_poster = customtkinter.CTkLabel(master=frm_movie_card, text='', wraplength=30)
            lbl_movie_poster.pack(pady=10, padx=10)
            asyncio.run(self.load_image(movie, lbl_movie_poster))
            lbl_movie_title = customtkinter.CTkLabel(master=frm_movie_card, text=movie.get('title'), wraplength=300)
            lbl_movie_title.pack(pady=10, padx=10)
            frm_movie_card.grid(row=count // self.result_columns, column=count % self.result_columns, padx=10, pady=10)
            count += 1

    async def load_image(self, movie, label):
        poster = self.parent.get_movie_poster(movie.get('poster_path'), size=1)
        img_poster = customtkinter.CTkImage(
            light_image=poster if poster is not None else self.default_poster,
            size=(200, 300)
        )
        label.configure(image=img_poster)
