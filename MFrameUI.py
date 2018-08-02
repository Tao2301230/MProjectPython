# Refer from https://stackoverflow.com/questions/26213549/switching-between-frames-in-tkinter-menu
from Tkinter import *
import Tkinter as tk
import ttk

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
        self.menu_bar.add_command(label='Parameter Space Summary',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Runtime Monitor',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

    def __aboutHandler(self):
        print "help handler"

'''
haven't implement 
    Checkbox: bind with Save Button
    Add to Template, Add to New File bind with 2 Entries and 1 ComboBox
    Table to show final parameter
'''
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
        self.menu_bar.add_command(label='Parameter Space Summary',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Runtime Monitor',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

        self.page_label = tk.Label(self, text='Spark Parameter Space')
        self.page_label.grid(row = 0, padx = 5, pady = 5, sticky = tk.W + tk.E)

        # Define from Template
        self.ps_DFT = tk.Label(self, text='Define from Template: ')
        self.ps_DFT.grid(row=1, padx=5, pady=5, sticky=tk.W + tk.E)

        '''
        Template: 
        parameter title,    parameter type,     parameter range,    Checkbox
        opt_level           IntegerParameter    0-3
        align-functions     EnumParameter       on | off | default
        align-jumps         EnumParameter       on | off | default
        align-labels        EnumParameter       on | off | default
        
        '''

        spark_PS = {'opt_level':['IntegerParameter', '0-3'],
                    'align-functions':['EnumParameter', 'on | off | default'],
                    'align-jumps':['EnumParameter', 'on | off | default'],
                    'align-labels':['EnumParameter', 'on | off | default']}

        col = 0
        for i in ['Parameter title', 'Parameter type', 'Parameter range', 'Option']:
            Label(self, text = i). grid(row=2, column=col)
            col += 1
        crow = 3
        col = 0
        var = StringVar()

        for k,v in spark_PS.items():
            Label(self, text=k).grid(row=crow, column=col)
            Label(self, text=v[0]).grid(row=crow, column=col+1)
            Label(self, text=v[1]).grid(row=crow, column=col+2)
            Checkbutton(self, variable=var).grid(row=crow, column=col+3)
            crow += 1


        self.ps_DFT_save = tk.Button(self, text='Save ')
        self.ps_DFT_save.grid(row=9, column=2, padx=5, pady=5,sticky=tk.W + tk.E)



        # Start From Scratch
        self.ps_SFS = tk.Label(self, text='Add Manually: ')
        self.ps_SFS.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_SFS_title = tk.Label(self, text='Parameter Title: ')
        self.ps_SFS_title.grid(row=12, padx=5, pady=5, sticky=tk.W + tk.E)

        self.parameter_title = tk.Entry(self)
        self.parameter_title.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_SFS_type = tk.Label(self, text='Parameter Type: ')
        self.ps_SFS_type.grid(row=13, padx=5, pady=5, sticky=tk.W + tk.E)

        pt = StringVar()
        self.parameter_type = ttk.Combobox(self, textvariable=pt)
        self.parameter_type['values']=('IntegerParameter', 'FloatParameter',
                                       'PowerOfTwoParameter', 'EnumParameter',
                                       'BooleanParameter', 'PermutationParameter')
        self.parameter_type['state']='readonly'
        self.parameter_type.current(0)
        # self.bind('')
        self.parameter_type.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_range = tk.Label(self, text='Range / Enum: ')
        self.ps_range.grid(row=14, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.parameter_range_max = tk.Entry(self, width=5)
        self.parameter_range_max.grid(row=14, column=1, padx=5, pady=5, sticky=tk.W + tk.E)


        self.ps_SFS_add = tk.Button(self, text='Add to Template')
        self.ps_SFS_add.grid(row=15, column=2, padx=5, pady=5,sticky=tk.W + tk.E)

        self.ps_SFS_add = tk.Button(self, text='Add to New File')
        self.ps_SFS_add.grid(row=16, column=2, padx=5, pady=5,sticky=tk.W + tk.E)



'''
haven't implement
    Add Button: bind with 2 RadioButtons
    Table to show final parameter
'''
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

        self.page_label = tk.Label(self, text='Hibench Parameter Space')
        self.page_label.grid(row = 0, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.workload_label = tk.Label(self, text = 'Select WorkLoad: ')
        self.workload_label.grid(row = 1, padx = 5, pady = 5, sticky = tk.W + tk.E)

        '''
        hibench.wordcount.tiny.datasize                 32000
        hibench.wordcount.small.datasize                320000000
        hibench.wordcount.large.datasize                3200000000
        hibench.wordcount.huge.datasize                 32000000000
        hibench.wordcount.gigantic.datasize             320000000000
        hibench.wordcount.bigdata.datasize              1600000000000
        '''

        self.workload = StringVar()
        col = 2

        for r in ('tiny', 'small', 'large', 'huge', 'gigantic', 'bigdata'):
            Radiobutton(self, variable = self.workload, text = r,
                        value = r).grid(row = 1, column = col)
            col += 2

        self.task_label = tk.Label(self, text='Select Task: ')
        self.task_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.hibench_task = StringVar()
        col = 2
        for r in ('WordCount', 'Sort', 'TeraSort', 'linear', 'SVD', 'KMeans', 'PageRank'):
            Radiobutton(self, variable = self.hibench_task, text = r,
                        value = r).grid(row = 2, column = col)
            col += 2

        self.submit_button = tk.Button(self, text = 'Add', command = self.button_click())
        self.submit_button.grid(row = 5, column = 5)


    def button_click(self):
        print self.workload
        print self.hibench_task


'''
haven't implement 
    Save Button: bind with 2 ComboBox and 1 Entry

'''
class OpentunerPSFrame(BaseFrame):

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
        self.menu_bar.add_command(label='Parameter Space Summary',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Runtime Monitor',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

        self.ot_st_label = Label(self, text='Search Technique: ')
        self.ot_st_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        st = StringVar()
        self.search_technique = ttk.Combobox(self, textvariable=st)
        self.search_technique['values'] = ('AUC Bandit', 'Other')
        self.search_technique['state'] = 'readonly'
        self.search_technique.current(0)
        # self.bind('')
        self.search_technique.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ot_limit_label = Label(self, text='Limit: ')
        self.ot_limit_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ot_limit = tk.Entry(self, text='limit')
        self.ot_limit.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        # Tune Condition
        self.ot_tc_label = Label(self, text='Tune Condition: ')
        self.ot_tc_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        tc = StringVar()
        self.tune_condition = ttk.Combobox(self, textvariable=tc)
        self.tune_condition['values'] = ('Time', 'Other')
        self.tune_condition['state'] = 'readonly'
        self.tune_condition.current(0)
        # self.bind('')
        self.tune_condition.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        # Save Button
        self.save_button = tk.Button(self, text='Save')
        self.save_button.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

'''
haven't implement 
    3 Summary table: 
    Spark Parameter, Hibench Parameter, Opentuner Parameter
'''

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
        self.menu_bar.add_command(label='Parameter Space Summary',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Runtime Monitor',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

        self.spark_summary_label = Label(self, text='Spark Summary: ')
        self.spark_summary_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        # table:

        self.hibench_summary_label = Label(self, text='Hibench Summary: ')
        self.hibench_summary_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        # table:

        self.opentuner_summary_label = Label(self, text='Opentuner Summary: ')
        self.opentuner_summary_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W + tk.E)


        self.submittasks = tk.Button(self, text='Submit Tasks')
        self.submittasks.grid(padx=5, pady=5, sticky=tk.W + tk.E)




class RuntimeFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label = 'Set Spark',
                                  command = lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label = 'Set HiBench',
                                  command = lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label = 'Set Opentuner',
                                  command = lambda: self.controller.show_frame(OpentunerPSFrame))
        self.menu_bar.add_command(label = 'Parameter Space Summary',
                                  command = lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label = 'Runtime Monitor',
                                  command = lambda: self.controller.show_frame(RuntimeFrame))



        # Example task ID table
        self.taskid_example = Label(self, text='Task1')
        self.taskid_example.grid(padx=5, pady=5, sticky=tk.W + tk.E)

        self.taskid_summary = Label(self, text='Parameter tuned: A, B, C Hibench Task: A, B, C Opentuner Parameter: A, B, C Parameter Tuned Result: A, B, C')
        self.taskid_summary.grid(padx=5, pady=5, sticky=tk.W + tk.E)

        self.top10_ps = PhotoImage(file='index.png')
        self.test_button = Button(self, image = self.top10_ps)
        self.test_button.grid(padx=5, pady=5, sticky=tk.W + tk.E)

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

