import tkinter as tk
from subprocess import PIPE, Popen, TimeoutExpired
from threading import Event, Thread
from tkinter import ttk


class ShellCommandDialog(tk.Toplevel):
    def __init__(self, master, command, **kwargs) -> None:
        super().__init__(master, **kwargs, padx="10", pady="10")
        self._command = command
        self._done = Event()
        self._setup_configuration()

    def center(self, width, height):
        x = int((self.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.winfo_screenheight() / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_configuration(self):
        self.center(400, 300)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, pad="5")
        self.rowconfigure(1, weight=1)

        if isinstance(self._command, list):
            cmd_str = " ".join(self._command)
        else:
            cmd_str = self._command

        self._cmd_text = tk.StringVar(value=cmd_str)
        self._cmd = ttk.Entry(
            self,
            textvariable=self._cmd_text,
            font=("Arial", 8),
            state="disabled",
        )
        self._cmd.grid(row=0, column=0, sticky=tk.EW)

        self._output = tk.Text(
            self, state="disabled", wrap="none", font=("Arial", 8)
        )
        self._output.grid(row=1, column=0, sticky=tk.NSEW)

        self.protocol("WM_DELETE_WINDOW", self._handle_close)
        self.transient(self.master)
        self.resizable(True, True)
        self.wait_visibility()
        self.grab_set()

        self._proc = Popen(self._command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self._thread = Thread(target=self._handle_proc, daemon=True)
        self._thread.start()

        self.wait_window()

    def _handle_proc(self):
        while not self._done.is_set():
            if self._proc.poll() is None:
                line = self._proc.stdout.readline().decode("utf-8")
                if line:
                    self._output["state"] = "normal"
                    self._output.insert("end", line)
                    self._output["state"] = "disabled"
                    self._output.see("end")
            else:
                self._done.set()

    def _handle_close(self):
        self._done.set()

        try:
            self._proc.terminate()
            self._proc.wait(2)
        except TimeoutExpired:
            self._proc.kill()

        try:
            self._thread.join(2)
        except TimeoutError:
            pass

        self.grab_release()
        self.destroy()
