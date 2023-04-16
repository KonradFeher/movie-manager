import pathlib
import customtkinter
from PIL import Image

from src.pages.Page import Page


class LoginPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager Login"

    @staticmethod
    def get_page_size():
        return "600x580"

    @staticmethod
    def get_page_min_size():
        return "390x561"

    def __init__(self, master: customtkinter.CTkFrame, controller, **kwargs):
        super().__init__(master, **kwargs)

        self.logo = customtkinter.CTkImage(
            light_image=Image.open(pathlib.Path("assets", "icon_1.png")),
            dark_image=Image.open(pathlib.Path("assets", "icon_2.png")),
            size=(200, 200)
        )
        self.lbl_logo = customtkinter.CTkLabel(master=self, image=self.logo, text="", corner_radius=25)
        self.lbl_logo.pack(anchor="center", pady=(50, 10), padx=30)

        self.lbl_username = customtkinter.CTkLabel(master=self, text="Username")
        self.lbl_username.pack(anchor="center", pady=(25, 0), padx=30)
        self.ent_username = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Username")
        self.ent_username.pack(anchor="center", pady=10, padx=30)

        self.lbl_password = customtkinter.CTkLabel(master=self, text="Password")
        self.lbl_password.pack(anchor="center", pady=0, padx=30)
        self.ent_password = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password", show="•")
        self.ent_password.pack(anchor="center", pady=10, padx=30)

        self.frm_buttons = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.frm_buttons.grid_rowconfigure(0, weight=1)  # configure grid system
        self.frm_buttons.grid_columnconfigure(0, weight=1)
        # self.frm_buttons.grid_columnconfigure(1, weight=1)
        self.frm_buttons.login_button = customtkinter.CTkButton(
            master=self.frm_buttons,
            width=200,
            height=40,
            corner_radius=20,
            text="Log In",
            command=controller.login_user
        )
        self.frm_buttons.login_button.grid(row=0, column=0, pady=5, padx=10)

        # self.frm_buttons.register_button = customtkinter.CTkButton(
        #     master=self.frm_buttons,
        #     width=200,
        #     height=40,
        #     corner_radius=20,
        #     text="Register",
        #     command=lambda: controller.show_page(RegisterPage)
        # )
        # self.frm_buttons.register_button.grid(row=0, column=1, pady=5, padx=10)
        self.frm_buttons.pack(anchor="center", pady=(25, 50), padx=20)

        self.btn_register = customtkinter.CTkButton(
            master=self,
            height=30,
            corner_radius=15,
            text='Register',
            command=lambda: controller.show_page("RegisterPage"),
            fg_color="#142d5e",
            text_color="#5584CC"
        )
        self.btn_register.place(anchor="nw", x=20, y=20)
