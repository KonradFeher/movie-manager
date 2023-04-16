import customtkinter
from src.models.User import User
from src.pages.Page import Page


class MainPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager"

    @staticmethod
    def get_page_size():
        return "920x740"

    def __init__(self, master: customtkinter.CTkFrame, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure('all', weight=1)
        self.grid_rowconfigure('all', weight=1)

