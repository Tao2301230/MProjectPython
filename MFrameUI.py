# Refer from https://stackoverflow.com/questions/26213549/switching-between-frames-in-tkinter-menu
from Tkinter import *
from Tkinter import ttk
import Tkinter as tk

class BaseFrame(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master = None)
        self.controller = controller
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label = 'Set Spark',
                                  command=lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label = 'Set HiBench',
                                  command=lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label = 'Set Opentuner',
                                  command=lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

    def __aboutHandler(self):
        print "help handler"


class SparkPSFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label='Set Spark',
                                  command=lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label='Set Opentuner',
                                  command=lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))



class HibenchPSFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label='Set Spark',
                                  command=lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label='Set Opentuner',
                                  command=lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

        self.workload_label = tk.Label(self, 'Select WorkLoad: ')
        self.workload_label.grid(padx=5, pady=5, sticky=tk.W + tk.E)

        workload = StringVar()
        self.workload_combobox =


class OpentunerPSFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label = 'Set Spark',
                                  command=lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label = 'Set HiBench',
                                  command=lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label = 'Set Opentuner',
                                  command=lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))


class PSSummaryFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label='Set Spark',
                                  command=lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label='Set Opentuner',
                                  command=lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))
        self.new_button = tk.Button(self)
        self.new_button.grid(padx=5, pady=5, sticky=tk.W + tk.E)


class RuntimeFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label = 'Set Spark',
                                  command=lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label = 'Set HiBench',
                                  command=lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label = 'Set Opentuner',
                                  command=lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Set HiBench',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

        self.new_text = tk.Entry(self)
        self.new_text.grid(padx=5, pady=5, sticky=tk.W + tk.E)


class MFrameUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Spark Tuner")
        self.create_widgets()
        self.resizable(0, 0)

    def create_widgets(self):
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.frames = {}
        for f in (SparkPSFrame, HibenchPSFrame,
                  OpentunerPSFrame, PSSummaryFrame,
                  RuntimeFrame):
            frame = f(self.container, self)
            frame.grid(row=60, column=50, sticky=tk.NW+tk.SE)
            self.frames[f] = frame
        self.show_frame(SparkPSFrame)

    def show_frame(self, cls):
        self.frames[cls].tkraise()

if __name__ == "__main__":
    app = MFrameUI()
    app.minsize(600, 500)
    app.mainloop()
    exit()

