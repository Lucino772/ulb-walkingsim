import os
import sys
from tkinter import *
from tkinter import messagebox, ttk

from loguru import logger

from gui.shell import ShellCommandDialog


class SimView(ttk.Frame):
    def __init__(self, master=None, **kwargs) -> None:
        logger.info("Setting up simulation view")
        logger.debug(f"master: {master}")
        logger.debug(f"kwargs: {kwargs}")
        logger.debug("Calling super().__init__(master, **kwargs)")

        super().__init__(master, **kwargs)
        # super().__init__()
        logger.debug("Calling self._setup_configuration()")
        self._setup_configuration()

        # Dynamic options callbacks
        self._algo_options_cbs = dict()
        self._algo_options_cbs["GA"] = self._show_ga_options
        self._algo_options_cbs["PPO"] = self._show_ppo_options
        self._current_algo_options = []

    def _setup_configuration(self):
        logger.info("Setting up simulation configuration")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, pad="20")
        self.rowconfigure(1, pad="20")
        self.rowconfigure(2, pad="20")
        self.rowconfigure(5, pad="20")
        self.rowconfigure(6, pad="20")
        self.rowconfigure(7, pad="20")
        # Environment selection
        self._env_select_label = ttk.Label(self, text="Environnement")
        self._env_select_label.grid(row=0, column=0, padx="0 10", sticky=W)
        self.__env_var = StringVar()
        self._env_select_field = ttk.Combobox(
            self, textvariable=self.__env_var
        )
        self._env_select_field["values"] = ["default", "moon", "mars"]
        self._env_select_field.grid(row=0, column=1, sticky=(W, E))

        # Creature config
        self._creature_select_lbl = ttk.Label(
            self, text="Choix de la créature"
        )
        self._creature_select_lbl.grid(row=1, column=0, padx="0 10", sticky=W)
        self.__creature_var = StringVar()
        self._creature_select_field = ttk.Combobox(
            self, textvariable=self.__creature_var
        )
        self._creature_select_field["values"] = ["quadrupede", "bipede"]
        self._creature_select_field.grid(row=1, column=1, sticky=(W, E))

        # Algorithm config
        self._algo_config_lbl = ttk.Label(
            self, text="Configuration algorithme d'apprentissage"
        )
        self._algo_config_lbl.grid(
            row=2, column=0, padx="0 10", columnspan=2, sticky=W
        )
        self._algo_select_lbl = ttk.Label(self, text="Choix de l'algorithme")
        self._algo_select_lbl.grid(row=3, column=0, padx="0 10", sticky=W)
        self.__algo_var = StringVar()
        self._algo_select_field = ttk.Combobox(
            self, textvariable=self.__algo_var
        )
        self._algo_select_field["values"] = ["GA", "PPO"]
        self._algo_select_field.grid(row=3, column=1, sticky=(W, E))

        self._algo_select_field.bind(
            "<<ComboboxSelected>>", self._handle_select_algo_field
        )

        # Sim Button
        self._sim_btn = ttk.Button(
            self,
            text="Simulate",
            command=self._handle_sim_btn,
        )
        self._sim_btn.grid(row=5, column=1, sticky=SE)

    @property
    def walkingsim_command(self):
        # NOTE: -u is important for showing the output in the dialog
        logger.info("Building walkingsim command")
        cmd = [sys.executable, "-u", "-m", "walkingsim", "train"]
        cmd += ["--environment", self.__env_var.get().lower()]
        cmd += ["--creature", self.__creature_var.get().lower()]
        cmd += ["--algorithm", self.__algo_var.get().lower()]

        if self.__algo_var.get() == "GA":
            cmd += ["--population", self.__ga_pop_var.get()]
            cmd += ["--generations", self.__ga_gen_var.get()]
        elif self.__algo_var.get() == "PPO":
            cmd += ["--timesteps", self.__ppo_iter_var.get()]

        return cmd

    def _handle_sim_btn(self):
        logger.info("Handling simulation button click")
        ShellCommandDialog(self, self.walkingsim_command)

    def _handle_select_algo_field(self, ev):
        self._algo_options_cbs[self.__algo_var.get()]()

    def _show_ga_options(self):
        logger.info("Showing GA options")
        self._hide_algo_options()

        self._ga_pop_lbl = ttk.Label(self, text="Taille population")
        self._ga_pop_lbl.grid(row=4, column=0, padx="0 10", sticky=W)
        self.__ga_pop_var = StringVar()
        self._ga_pop_field = ttk.Entry(self, textvariable=self.__ga_pop_var)
        self._ga_pop_field.grid(row=4, column=1, sticky=(W, E))

        self._ga_gen_lbl = ttk.Label(self, text="Nombre de générations")
        self._ga_gen_lbl.grid(row=5, column=0, padx="0 10", sticky=W)
        self.__ga_gen_var = StringVar()
        self._ga_gen_field = ttk.Entry(self, textvariable=self.__ga_gen_var)
        self._ga_gen_field.grid(row=5, column=1, sticky=(W, E))

        self._current_algo_options.extend(
            [
                self._ga_pop_lbl,
                self._ga_pop_field,
                self._ga_gen_lbl,
                self._ga_gen_field,
            ]
        )

    def _show_ppo_options(self):
        self._hide_algo_options()

        self._ppo_iter_lbl = ttk.Label(self, text="Nombre d'itérations")
        self._ppo_iter_lbl.grid(row=4, column=0, padx="0 10", sticky=W)
        self.__ppo_iter_var = StringVar()
        self._ppo_iter_field = ttk.Entry(
            self, textvariable=self.__ppo_iter_var
        )
        self._ppo_iter_field.grid(row=4, column=1, sticky=(W, E))

        self._current_algo_options.extend(
            [self._ppo_iter_lbl, self._ppo_iter_field]
        )

    def _hide_algo_options(self):
        for opt in self._current_algo_options:
            opt.grid_forget()

    def _add_debug_borders(self, elem):
        elem["borderwidth"] = 3
        elem["relief"] = "solid"
