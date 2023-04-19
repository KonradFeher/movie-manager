import math
import pathlib
from tkinter import LEFT, RIGHT, TOP, BOTTOM

import customtkinter
from PIL import Image


class MovieFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.default_poster = Image.open(pathlib.Path("assets", "icon.png"))
        self.controller = controller
        self.result_columns = 3
        self.movie = None

        self.lbl_background = customtkinter.CTkLabel(master=self, text="")
        self.lbl_background.place(x=0, y=0)
        self.lbl_poster = customtkinter.CTkLabel(master=self, text="")
        self.lbl_poster.place(x=50, y=50)

        self.lbl_title = customtkinter.CTkLabel(master=self, text="Movie Title", font=("Roboto", 30, "bold"))
        self.lbl_title.pack(anchor="e", pady=5, padx=20)

        self.lbl_original_title = customtkinter.CTkLabel(master=self, text="original_title", font=("Roboto", 12),
                                                         wraplength=300, justify="right")
        self.lbl_original_title.pack(anchor="e", pady=5, padx=20)

        self.lbl_tagline = customtkinter.CTkLabel(master=self, text="tagline", font=("Roboto", 12), wraplength=300,
                                                  justify="right")
        self.lbl_tagline.pack(anchor="e", pady=5, padx=20)

        self.lbl_runtime = customtkinter.CTkLabel(master=self, text="runtime", font=("Roboto", 12), wraplength=300,
                                                  justify="right")
        self.lbl_runtime.pack(anchor="e", pady=5, padx=20)

        self.lbl_overview = customtkinter.CTkLabel(master=self, text="Overview", font=("Roboto", 12), wraplength=300,
                                                   justify="right")
        self.lbl_overview.pack(anchor="e", pady=5, padx=20)

        self.lbl_budget = customtkinter.CTkLabel(master=self, text="budget", font=("Roboto", 12), wraplength=300,
                                                 justify="right")
        self.lbl_budget.pack(anchor="e", pady=5, padx=20)

        self.lbl_revenue = customtkinter.CTkLabel(master=self, text="revenue", font=("Roboto", 12), wraplength=300,
                                                  justify="right")
        self.lbl_revenue.pack(anchor="e", pady=5, padx=20)

        self.lbl_vote_average = customtkinter.CTkLabel(master=self, text="vote_average", font=("Roboto", 12),
                                                       wraplength=300, justify="right")
        self.lbl_vote_average.pack(anchor="e", pady=5, padx=20)

        self.lbl_vote_count = customtkinter.CTkLabel(master=self, text="vote_count", font=("Roboto", 12),
                                                     wraplength=300, justify="right")
        self.lbl_vote_count.pack(anchor="e", pady=5, padx=20)

        self.lbl_genres = customtkinter.CTkLabel(master=self, text="genres", font=("Roboto", 12),
                                                 wraplength=300, justify="right")
        self.lbl_genres.pack(anchor="e", pady=5, padx=20)

        self.btn_watchlist = customtkinter.CTkButton(
            master=self, text="Add to Watchlist",
            font=("Roboto", 20, "bold"),
            bg_color="transparent",
            command=lambda: controller.add_to_watchlist(self.movie))
        self.btn_watchlist.pack(anchor="e", pady=5, padx=20)

        self.btn_watched_it = customtkinter.CTkButton(
            master=self, text="Watched it!",
            font=("Roboto", 20, "bold"),
            bg_color="transparent",
            command=lambda:  controller.add_to_watched(self.movie))
        self.btn_watched_it.pack(anchor="e", pady=5, padx=20)

    def load_movie(self, movie):
        # movie = self.controller.api.fetch_movies("The Big Lebowski").get('results')[0]
        print(movie)
        self.movie = movie

        # todo: link up buttons, GRID IT UP
        self.lbl_title.configure(text=f'{movie.get("title")}\n'
                                      f'({movie.get("release_date").split("-")[0]})')

        backdrop_image = self.controller.get_movie_image(movie.get('backdrop_path'), typ='backdrop', size=-1)
        poster_image = self.controller.get_movie_image(movie.get('poster_path'), typ='poster', size=-1)
        pil = backdrop_image or poster_image or None
        if pil is not None:
            pil.putalpha(10)
            image = customtkinter.CTkImage(
                light_image=pil,
                size=(self._current_width, math.floor(pil.height * self._current_width / pil.width))
            )
            self.lbl_background.configure(image=image)
        pil = poster_image or None
        if pil is not None:
            image = customtkinter.CTkImage(
                light_image=pil,
                size=(200, math.floor(pil.height * 200 / pil.width))
            )
            self.lbl_poster.configure(image=image)

        self.lbl_overview.configure(text=f'{movie.get("overview")}')
        self.lbl_original_title.configure(
            text=f'{movie.get("original_title")} ({movie.get("original_language").upper()})')
        self.lbl_tagline.configure(text=f'"{movie.get("tagline")}"', font=("Roboto", 15, "italic"))
        self.lbl_runtime.configure(text=f'Runtime\n'
                                        f'{movie.get("runtime")} minutes')
        self.lbl_overview.configure(text=f'{movie.get("overview")}')
        self.lbl_budget.configure(text=f'Budget\n'
                                       f'${"{:,}".format(int(movie.get("budget"))).replace(",", " ")}')
        self.lbl_revenue.configure(text=f'Revenue\n'
                                        f'${"{:,}".format(int(movie.get("revenue"))).replace(",", " ")}')
        self.lbl_vote_average.configure(text=f'Average Rating\n'
                                             f'{movie.get("vote_average")}')
        self.lbl_vote_count.configure(text=f'Rating Count\n'
                                           f'{movie.get("vote_count")}')
        self.lbl_genres.configure(text=f'Genres\n{", ".join([x["name"] for x in movie.get("genres")])}')
