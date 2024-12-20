import customtkinter as ctk

from components.new_account import NewAccount
from components.export_import import ExportImport
from components.table import Table
from custom_widgets import Entry, Frame, Label, Button
from utility.constants import *

_SEARCH_PLACEHOLDER_TEXT = "Search accounts..."


class Home(ctk.CTkFrame):

    def __init__(self, root: ctk.CTk) -> None:
        self.__root = root
        super().__init__(self.__root)
        # Create a search variable to bind on change event
        self.__search_var = ctk.StringVar()
        # Create header widgets: search & user options
        self.__create_header()
        # Render the table
        self.__show_account_details()

        self.configure(bg_color=WINDOW["bg"], fg_color=WINDOW["bg"])
        self.grid(column=0, row=0, sticky="news", padx=50, pady=(30, 55))
        self.grid_columnconfigure(0, weight=1)

    def __create_header(self) -> None:

        # Create a header wrapper
        container = Frame(self)
        container.grid(column=0, row=1, sticky="ew", pady=(20, 0))

        # Create header and subheading wrapper
        label_container = Frame(container)
        label_container.grid(column=0, row=0, sticky="w", pady=(0, 40))

        heading = Label(
            label_container,
            title="Your Secure Vault",
            text_color=TEXT["dark"],
            font_size=24,
        )
        heading.grid(column=0, row=0, sticky="w")

        subheading = Label(
            label_container,
            title="Easily manage and access all your passwords and sensitive information.",
            text_color=TEXT["light"],
        )
        subheading.grid(column=0, row=1, sticky="w")

        # Create search box
        self.__search_entry = Entry(
            container,
            text_variable=self.__search_var,
            text_color=TEXT["light"],
        )
        self.__search_entry.grid(column=0, row=1, sticky="nwse")
        # Workaround to show placeholder
        self.__search_entry.insert(0, _SEARCH_PLACEHOLDER_TEXT)
        self.__search_entry.bind("<FocusIn>", self.__clear_placeholder)
        self.__search_entry.bind("<FocusOut>", self.__show_placeholder)

        # Create user options
        for idx, (key, val) in enumerate(USER_OPTIONS.items()):
            button = Button(
                container,
                command=lambda key=key: self.__navigate_to(key),
                title=val["title"],
            )
            button.grid(column=idx + 1, row=1, sticky="e", padx=(10, 0))

        container.grid_columnconfigure(0, weight=1)

    def __show_account_details(self) -> None:

        table_container = Frame(self, bg="red")
        table_container.grid(column=0, row=2, sticky="news", pady=(40, 0))
        # Create table
        self.table = Table(self.__root, table_container, self.__search_var)

        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def __navigate_to(self, key: str) -> None:
        if key == "new":
            _ = NewAccount(self.__root, self.table.refresh)
        elif key == "exp-imp":
            _ = ExportImport(self.__root, self.table.refresh)
        else:
            pass

    def __clear_placeholder(self, _):
        """
        Workaround: Clear search widget placeholder
        """
        widget = self.__search_entry
        if Table.show_search_placeholder:
            widget.delete(0, ctk.END)
            widget.configure(text_color=TEXT["dark"])
            Table.show_search_placeholder = False

    def __show_placeholder(self, _):
        """
        Workaround: Show search widget placeholder
        """
        widget = self.__search_entry
        if widget.get() == "":
            Table.show_search_placeholder = True
            widget.configure(text_color=TEXT["light"])
            widget.insert(0, _SEARCH_PLACEHOLDER_TEXT)
