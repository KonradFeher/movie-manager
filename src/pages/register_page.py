import pathlib
from tkinter import BOTTOM, END

import customtkinter
from PIL import Image
from .page import Page


class RegisterPage(customtkinter.CTkFrame, Page):

    @staticmethod
    def get_page_title():
        return "MovieManager Register"

    @staticmethod
    def get_page_size():
        return "600x750"

    @staticmethod
    def get_page_min_size():
        return "462x750"

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
        self.ent_username = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="The_Dude")
        self.ent_username.pack(anchor="center", pady=10, padx=30)

        self.lbl_email = customtkinter.CTkLabel(master=self, text="E-mail Address")
        self.lbl_email.pack(anchor="center", pady=0, padx=30)
        self.ent_email = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="jeffrey_lebowski@gmail.com")
        self.ent_email.pack(anchor="center", pady=10, padx=30)

        self.lbl_password = customtkinter.CTkLabel(master=self, text="Password")
        self.lbl_password.pack(anchor="center", pady=0, padx=30)
        self.ent_password = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password", show="•")
        self.ent_password.pack(anchor="center", pady=10, padx=30)

        self.lbl_password_again = customtkinter.CTkLabel(master=self, text="Password Confirmation")
        self.lbl_password_again.pack(anchor="center", pady=0, padx=30)
        self.ent_password_again = customtkinter.CTkEntry(master=self, width=400, corner_radius=5, placeholder_text="Password Confirmation", show="•")
        self.ent_password_again.pack(anchor="center", pady=10, padx=30)

        self.lbl_errors = customtkinter.CTkLabel(master=self, text="", corner_radius=25, text_color="red")
        self.lbl_errors.pack(anchor="center")

        self.register_button = customtkinter.CTkButton(
            master=self,
            width=200,
            height=40,
            corner_radius=20,
            text="Register",
            command=lambda: controller.register_user()
        )
        self.register_button.pack(side=BOTTOM, anchor="center", pady=(25, 25), padx=20)

        self.btn_back = customtkinter.CTkButton(
            master=self,
            height=30,
            corner_radius=15,
            text='Back',
            command=lambda: controller.show_page("LoginPage"),
            fg_color="#142d5e",
            text_color="#5584CC"
        )
        self.btn_back.place(anchor="nw", x=20, y=20)

    def display_errors(self, errors):
        error_text = ""
        for error in errors:
            error_text += error + '\n'
        self.lbl_errors.configure(text=error_text)

    def clear_form(self):
        self.ent_username.delete(0, END)
        self.ent_email.delete(0, END)
        self.ent_password.delete(0, END)
        self.ent_password_again.delete(0, END)
