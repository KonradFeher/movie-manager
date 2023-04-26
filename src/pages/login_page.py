import pathlib
from tkinter import BOTTOM, END

import customtkinter
from PIL import Image
from src.pages.page import Page


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

        self.lbl_username_or_email = customtkinter.CTkLabel(master=self, text="Username or email")
        self.lbl_username_or_email.pack(anchor="center", pady=(25, 0), padx=30)
        self.ent_username_or_email = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Username or email")
        self.ent_username_or_email.pack(anchor="center", pady=10, padx=30)

        self.lbl_password = customtkinter.CTkLabel(master=self, text="Password")
        self.lbl_password.pack(anchor="center", pady=0, padx=30)
        self.ent_password = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password", show="•")
        self.ent_password.pack(anchor="center", pady=10, padx=30)

        self.frm_buttons = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.frm_buttons.grid_rowconfigure(0, weight=1)  # configure grid system
        self.frm_buttons.grid_columnconfigure(0, weight=1)
        self.frm_buttons.login_button = customtkinter.CTkButton(
            master=self.frm_buttons,
            width=200,
            height=40,
            corner_radius=20,
            text="Log In",
            command=lambda: controller.login_user()
        )
        self.frm_buttons.login_button.grid(row=0, column=0, pady=5, padx=10)

        self.lbl_incorrect = customtkinter.CTkLabel(master=self, text="", corner_radius=25, text_color="red")
        self.lbl_incorrect.pack(anchor="center")

        self.frm_buttons.pack(side=BOTTOM, anchor="center", pady=(25, 25), padx=20)

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

    def display_incorrect(self, show=True):
        self.lbl_incorrect.configure(text="Invalid credentials." if show else "")

    def clear_form(self):
        self.ent_username_or_email.delete(0, END)
        self.ent_password.delete(0, END)
