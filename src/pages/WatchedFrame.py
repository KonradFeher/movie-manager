import asyncio
import pathlib
import customtkinter
from PIL import Image


class WatchedFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.default_poster = Image.open(pathlib.Path("assets", "icon.png"))
        self.controller = controller
        self.result_columns = 3
        self.lbl_movie_title = customtkinter.CTkLabel(master=self, text="Watched movies", width=500)
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
            command=lambda: controller.search_watched(self.ent_movie_title.get())
            # TODO
        )
        self.btn_search.pack(pady=(20, 20))

        self.frm_results = customtkinter.CTkScrollableFrame(master=self, height=555)
        self.frm_results.grid_rowconfigure("all", weight=1)
        for i in range(self.result_columns):
            self.frm_results.grid_columnconfigure(i, weight=1)
        self.frm_results.pack(fill='both', expand=True, padx=10, pady=10)
        self.results = list()

    def reset_results_frame(self):
        self.clear_results()
        self.frm_results.pack_forget()
        self.frm_results.destroy()
        self.frm_results = customtkinter.CTkScrollableFrame(master=self, height=555)
        self.frm_results.grid_rowconfigure("all", weight=1)
        for i in range(self.result_columns):
            self.frm_results.grid_columnconfigure(i, weight=1)
        self.frm_results.pack(fill='both', expand=True, padx=10, pady=10)
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
            # create card for movie
            frm_movie_card = customtkinter.CTkFrame(master=self.frm_results, width=150, height=300)

            lbl_movie_poster = customtkinter.CTkLabel(master=frm_movie_card, text='')
            lbl_movie_poster.pack(pady=10, padx=10)

            # set image asynchronously
            asyncio.run(self.load_image(movie, lbl_movie_poster))

            label_text = f"{movie.get('title')} ({movie.get('release_date').split('-')[0]})"
            lbl_movie_title = customtkinter.CTkLabel(master=frm_movie_card, text=label_text, wraplength=220)
            lbl_movie_title.pack(pady=10, padx=10)

            frm_movie_card.grid(row=count // self.result_columns, column=count % self.result_columns, padx=10,
                                pady=10)

            asyncio.run(self.set_handlers(movie, lbl_movie_poster, lbl_movie_title, frm_movie_card))
            count += 1

        if count == 0:
            print("no results found")
            lbl_no_results = customtkinter.CTkLabel(master=self.frm_results, text='No results.')
            lbl_no_results.grid(row=0, column=1, pady=10)

    async def set_handlers(self, movie, lbl_movie_poster, lbl_movie_title, frm_movie_card):
        # 'bind_all' is not allowed, could result in undefined behavior ????????????

        def button1(e, mov=movie):
            # print(mov.get('title'))
            self.controller.show_movie(movie)

        lbl_movie_poster.bind("<Button-1>", button1)
        lbl_movie_title.bind("<Button-1>", button1)
        frm_movie_card.bind("<Button-1>", button1)

        def enter(e, card=frm_movie_card):
            card.configure(fg_color="#666")

        lbl_movie_poster.bind("<Enter>", enter)
        lbl_movie_title.bind("<Enter>", enter)
        frm_movie_card.bind("<Enter>", enter)

        fg = frm_movie_card.cget("fg_color")

        def leave(e, card=frm_movie_card, fgc=fg):
            card.configure(fg_color=fgc)

        lbl_movie_poster.bind("<Leave>", leave)
        lbl_movie_title.bind("<Leave>", leave)
        frm_movie_card.bind("<Leave>", leave)

    async def load_image(self, movie, label):
        poster = self.controller.get_movie_image(movie.get('poster_path'), size=2)
        img_poster = customtkinter.CTkImage(
            light_image=poster if poster is not None else self.default_poster,
            size=(200, 300)
        )
        label.configure(image=img_poster)
