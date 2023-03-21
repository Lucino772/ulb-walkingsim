import os
from tkinter import *
from tkinter import ttk

from loguru import logger

from gui.sim import SimView
from gui.vis import VisView


class App:
    def __init__(self):
        logger.info("Starting app")
        self.__root = Tk()
        self.__root.title("3D walking simulator")
        self.center(500, 400)
        self.setup_tabs()

        # XXX DEBUG
        self._add_debug_borders()

    def center(self, width, height):

        x = int((self.__root.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.__root.winfo_screenheight() / 2) - (height / 2))
        self.__root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_tabs(self):
        logger.info("Setting up tabs")
        self.__content = ttk.Frame(self.__root, padding="10 10 10 10")
        self.__content.place(relwidth=1, relheight=1)
        self.__content.columnconfigure(0, weight=1)
        self.__content.rowconfigure(1, weight=1)

        self.__win_title = ttk.Label(
            self.__content, text="3D Walking simulator", padding=" 20 0 20 0"
        )
        self.__win_title.grid(row=0, column=0)

        self.__tabs = ttk.Notebook(self.__content)
        self.__tabs.grid(row=1, column=0, sticky=NSEW)

        self.__sim_tab = SimView(
            self.__tabs, relief="ridge", padding="5 5 5 5"
        )
        self.__tabs.add(self.__sim_tab, text="Simulation")

        self.__vis_tab = VisView(
            self.__tabs, relief="ridge", padding="5 5 5 5"
        )
        self.__tabs.add(self.__vis_tab, text="Visualisation")

    def _add_debug_borders(self):
        logger.info("Adding debug borders")
        for e in self.__content, self.__win_title:
            e["borderwidth"] = 3
            e["relief"] = "solid"

    def run(self):
        logger.info("Running app")
        self.__root.mainloop()


if __name__ == "__main__":
    app = App().run()
