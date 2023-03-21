import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from gui.shell import ShellCommandDialog


class VisView(ttk.Frame):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._setup_configuration()

    def _setup_configuration(self):
        self.rowconfigure(0, pad="5")
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, pad="5")
        self.columnconfigure(1, weight=1)

        # Algo Select
        ttk.Label(self, text="Algorithm:").grid(row=0, column=0, padx="0 10")
        self._selected_algo_var = tk.StringVar()
        self._select_algo_field = ttk.Combobox(
            self, textvariable=self._selected_algo_var
        )
        self._select_algo_field["values"] = ("GA", "PPO")
        self._select_algo_field.bind(
            "<<ComboboxSelected>>", self._handle_select_algo_field
        )
        self._select_algo_field.grid(row=0, column=1, sticky=tk.EW)

        # Solutions Files
        ttk.Label(self, text="Solutions").grid(
            row=1, column=0, columnspan=2, sticky=tk.EW
        )
        self._solutions_var = tk.StringVar()
        self._solutions_lbox = tk.Listbox(
            self, listvariable=self._solutions_var
        )
        self._solutions_lbox.bind(
            "<<ListboxSelect>>", self._handle_selected_solution
        )
        self._solutions_lbox.grid(
            row=2, column=0, columnspan=2, sticky=tk.NSEW
        )

        # Vis Button
        self._vis_btn = ttk.Button(
            self,
            text="Visualize",
            command=self._handle_vis_btn,
            state="disabled",
        )
        self._vis_btn.grid(row=3, column=1, sticky=tk.SE)

    @property
    def selected_algo(self):
        return self._selected_algo_var.get().lower()

    @property
    def selected_solution(self):
        indexes = self._solutions_lbox.curselection()
        if len(indexes) == 0:
            return None

        return self._solutions_lbox.get(indexes[0])

    @property
    def walkingsim_command(self):
        # NOTE: -u is important for showing the output in the dialog
        cmd = [sys.executable, "-u", "-m", "walkingsim", "visualize"]
        if self.selected_algo is not None:
            cmd += ["--algorithm", self.selected_algo]

        if self.selected_solution is not None:
            cmd += [self.selected_solution]

        return cmd

    def _handle_select_algo_field(self, ev):
        rootdir = os.path.join("solutions", self.selected_algo)
        if os.path.exists(rootdir):
            self._solutions_var.set(os.listdir(rootdir))
        else:
            self._solutions_var.set([])

        self._vis_btn.state(["disabled"])

    def _handle_selected_solution(self, ev):
        if len(self._solutions_lbox.curselection()) > 0:
            self._vis_btn.state(["!disabled"])

    def _handle_vis_btn(self):
        if self.selected_solution is None:
            messagebox.showwarning(
                title="No Solution", message="You must select a solution"
            )
        else:
            ShellCommandDialog(self, self.walkingsim_command)
