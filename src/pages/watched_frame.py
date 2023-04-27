import pathlib
import customtkinter
from PIL import Image

from .main_frame import MainFrame


# used to display current user's watched movies
class WatchedFrame(MainFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, **kwargs)

        self.default_poster = Image.open(pathlib.Path("assets", "icon.png"))
        self.controller = controller
        self.result_columns = 3

        self.lbl_page_title = customtkinter.CTkLabel(master=self, text="My Watched Movies", font=('Roboto', 22, 'bold'))
        self.lbl_page_title.pack(pady=10)
