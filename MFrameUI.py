# Refer from https://stackoverflow.com/questions/26213549/switching-between-frames-in-tkinter-menu

import adddeps
from Tkinter import *
import Tkinter as tk
import PIL
from PIL import ImageTk, Image
import ttk
from spark_tuner import GccFlagsTuner
import opentuner
import gl
from RuntimeSummary import show_summary

# Global Variable



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

        self.menu_bar.add_command(label='Parameter Space Summary',
                                  command=lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label='Runtime Monitor',
                                  command=lambda: self.controller.show_frame(RuntimeFrame))

    def __aboutHandler(self):
        print "help handler"

'''
completed: 
    Checkbox: bind with Save Button
    Add to Template, Add to New File bind with 2 Entries and 1 ComboBox
    Table to show final parameter

haven't implement          

more:
    validation:
        title: validate based on the version of Spark
        type bind with range
'''
class SparkPSFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

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
        # it can be read from a json file
        spark_PS = {'early-inlining-insns': ['IntegerParameter', '0-10'],
                    'align-functions':['EnumParameter', 'on|off|default'],
                    'align-jumps':['EnumParameter', 'on|off|default'],
                    'align-labels':['EnumParameter', 'on|off|default']}

        col = 0
        for i in ['Parameter title', 'Parameter type', 'Parameter range', 'Option']:
            Label(self, text = i). grid(row=2, column=col)
            col += 1
        crow = 3
        col = 0


        self.spark_ps=[] # Store the final result
        self.cb_vars=[]

        for k,v in spark_PS.items():
            var = IntVar()
            Label(self, text=k).grid(row=crow, column=col)
            Label(self, text=v[0]).grid(row=crow, column=col+1)
            Label(self, text=v[1]).grid(row=crow, column=col+2)
            cb = Checkbutton(self, variable=var)
            cb.grid(row=crow, column=col+3)
            self.cb_vars.append(var)
            self.spark_ps.append(k + ' ' + v[0] + ' ' + v[1])
            crow += 1

        self.ps_DFT_save = Button(self, text='Save', command=self.save_template)
        self.ps_DFT_save.grid(row=9, column=2, padx=5, pady=5,sticky=tk.W + tk.E)



        # Start From Scratch
        self.ps_SFS = Label(self, text='Add Manually: ')
        self.ps_SFS.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_SFS_title = Label(self, text='Parameter Title: ')
        self.ps_SFS_title.grid(row=12, padx=5, pady=5, sticky=tk.W + tk.E)

        self.parameter_title_var = StringVar()
        self.parameter_title = Entry(self, textvariable=self.parameter_title_var)
        self.parameter_title.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_SFS_type = Label(self, text='Parameter Type: ')
        self.ps_SFS_type.grid(row=13, padx=5, pady=5, sticky=tk.W + tk.E)

        self.pt = StringVar()
        self.parameter_type = ttk.Combobox(self, textvariable=self.pt)
        self.parameter_type['values']=('IntegerParameter', 'FloatParameter',
                                       'PowerOfTwoParameter', 'EnumParameter',
                                       'BooleanParameter', 'PermutationParameter')
        self.parameter_type['state']='readonly'
        self.parameter_type.current(0)
        # self.bind('')
        self.parameter_type.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W + tk.E)


        self.ps_range = Label(self, text='Range / Enum: ')
        self.ps_range.grid(row=14, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.pr = StringVar()
        self.parameter_range = Entry(self, textvariable=self.pr)
        self.parameter_range.grid(row=14, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_SFS_add = Button(self, text='Add to Template', command=self.add_to_template)
        self.ps_SFS_add.grid(row=11, column=2, padx=5, pady=5,sticky=tk.W + tk.E)

        self.ps_SFS_add = Button(self, text='Create Blank Draft', command=self.create_new_file)
        self.ps_SFS_add.grid(row=11, column=3, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ps_SFS_add = Button(self, text='Add to New File', command=self.add_to_new_file)
        self.ps_SFS_add.grid(row=11, column=4, padx=5, pady=5,sticky=tk.W + tk.E)

    def save_template(self):
        result = [i.get() for i in self.cb_vars]
        final_spark_ps = [self.spark_ps[i] for i in range(len(result)) if result[i]==1]

        for item in final_spark_ps:
            s=item.split()
            gl.spark_parameter[s[0]] = [s[1],s[2]]
        print gl.spark_parameter

        self.ps_add = Label(self, text='Successfully Added: ')
        self.ps_add.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        added_item = Label(self, text=', '.join(list(gl.spark_parameter.keys())))
        added_item.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W + tk.E)


    def add_to_template(self):
        # global gl.spark_parameter
        self.ps_add = Label(self, text='Successfully Added')
        self.ps_add.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        result = [i.get() for i in self.cb_vars]
        final_spark_ps = [self.spark_ps[i] for i in range(len(result)) if result[i] == 1]

        for item in final_spark_ps:
            s = item.split()
            gl.spark_parameter[s[0]] = [s[1], s[2]]

        gl.spark_parameter[self.parameter_title_var.get()]=[self.pt.get(), self.pr.get()]

        added_item = Label(self, text=', '.join(list(gl.spark_parameter.keys())))
        added_item.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W + tk.E)


    def create_new_file(self):
        # global gl.spark_parameter
        gl.spark_parameter.clear()
        self.ps_add = Label(self, text='Successfully Created: ')
        self.ps_add.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        added_item = Label(self, text=', '.join(list(gl.spark_parameter.keys())))
        added_item.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

    def add_to_new_file(self):
        # global gl.spark_parameter
        gl.spark_parameter[self.parameter_title_var.get()] = [self.pt.get(), self.pr.get()]

        self.ps_add = Label(self, text='Successfully Added: ')
        self.ps_add.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        added_item = Label(self, text=', '.join(list(gl.spark_parameter.keys())))
        added_item.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W + tk.E)


'''
Complete
    Add Button: bind with 2 RadioButtons
    Table to show final parameter
'''
class HibenchPSFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

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

        self.workload=StringVar()
        self.hibench_task = StringVar()

        col = 2

        for r in ('tiny', 'small', 'large', 'huge', 'gigantic', 'bigdata'):
            Radiobutton(self, variable = self.workload, text = r, value = r).grid(row = 1, column = col)
            col += 2

        self.task_label = tk.Label(self, text='Select Task: ')
        self.task_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.W + tk.E)

        col = 2
        for r in ('WordCount', 'Sort', 'TeraSort', 'linear', 'SVD', 'KMeans', 'PageRank'):
            Radiobutton(self, variable = self.hibench_task, text = r, value = r).grid(row = 2, column = col)
            col += 2

        # Set Opentuner

        Label(self, text='OpenTuner Parameter Space').grid(row=4)

        self.ot_st_label = Label(self, text='Search Technique: ')
        self.ot_st_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.st = StringVar()
        self.search_technique = ttk.Combobox(self, textvariable=self.st)
        self.search_technique['values'] = ('AUC Bandit', 'Other')
        self.search_technique['state'] = 'readonly'
        self.search_technique.current(0)
        # self.bind('')
        self.search_technique.grid(row=5, column=2, columnspan=4, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ot_limit_label = Label(self, text='Trials Threshold: ')
        self.ot_limit_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.ot_limit = tk.Entry(self, text='limit')
        self.ot_limit.grid(row=6, column=2, columnspan=4, padx=5, pady=5, sticky=tk.W + tk.E)

        # Tune Condition
        self.ot_tc_label = Label(self, text='Tune Condition: ')
        self.ot_tc_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.tc = StringVar()
        self.tune_condition = ttk.Combobox(self, textvariable=self.tc)
        self.tune_condition['values'] = ('Time', 'Other')
        self.tune_condition['state'] = 'readonly'
        self.tune_condition.current(0)
        # self.bind('')
        self.tune_condition.grid(row=7, column=2, columnspan=4, padx=5, pady=5, sticky=tk.W + tk.E)

        # Save Button
        # self.save_button = tk.Button(self, text='Save', command=self.save_opentuner)
        # self.save_button.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        self.submit_button = tk.Button(self, text = 'Add', command = self.add_task)
        self.submit_button.grid(row = 8, column = 7)

        Label(self, text='Task Summary: ').grid(row=10)

    def add_task(self):
        hbvalue = []
        hbvalue.append(self.workload.get())
        hbvalue.append(self.hibench_task.get())

        otvalue = []
        otvalue.append(self.search_technique.get())
        otvalue.append(self.ot_limit.get())
        otvalue.append(self.tune_condition.get())


        # global gl.task_id, gl.hibench_parameter
        gl.hibench_parameter.append(hbvalue)
        gl.opentuner_parameter.append(otvalue)

        hblabel = Label(self, text='Task' + str(gl.task_id) + ': ' + gl.hibench_parameter[gl.task_id][1]
                         + ', Workload: '+ gl.hibench_parameter[gl.task_id][0])\
            .grid(column=2, columnspan=6)

        Label(self, text='Task limits: ' + gl.opentuner_parameter[gl.task_id][1])\
            .grid(column=2, columnspan=6)
        print "finish add task"
        gl.task_id += 1


'''
complete implement 
    3 Summary table: 
    Spark Parameter, Hibench Parameter, Opentuner Parameter
'''

class PSSummaryFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.flash_PS = tk.Button(self, text='Update Summary', command=self.flash_parameter_summary)
        self.flash_PS.grid(row=0, column=0, padx = 5, pady = 5, sticky = tk.W + tk.E)

        self.submittasks = tk.Button(self, text='Submit Tasks', command=self.test)
        self.submittasks.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W + tk.E)

    def flash_parameter_summary(self):

        self.spark_summary_label = Label(self, text='Spark Summary: ')
        self.spark_summary_label.grid(column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        # global gl.spark_parameter, gl.hibench_parameter, gl.opentuner_parameter

        print len(gl.spark_parameter), len(gl.hibench_parameter), len(gl.opentuner_parameter)

        for i in gl.spark_parameter:
            Label(self, text=str(i)).grid(column=3)

        # table:

        self.hibench_summary_label = Label(self, text='Hibench Summary: ')
        self.hibench_summary_label.grid(column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        # table:
        for index, value in enumerate(gl.hibench_parameter):
            Label(self, text='Task ' + str(index)
                             + ': Task: '+ value[1]
                             + ', Workload: ' + value[0]).grid(column=3)

        self.opentuner_summary_label = Label(self, text='Opentuner Summary: ')
        self.opentuner_summary_label.grid(column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        for i in gl.opentuner_parameter:
            Label(self, text='Search Tech: ' + str(i[0])
                             + ', Job Time limits: ' + str(i[1])
                             + ', Tune Type: ' + str(i[2])).grid(column=3)

    def test(self):

        #default parameter:
        # --bail_threshold=500 --database=None --display_frequency=10 \
        # --generate_bandit_technique=False --label=None --list_techniques=False \
        # --machine_class=None --no_dups=False --parallel_compile=False \
        # --parallelism=4 --pipelining=0 --print_params=False \
        # --print_search_space_size=False --quiet=False --results_log=None \
        # --results_log_details=None --seed_configuration=[] --stop_after=None \
        # --technique=None --test_limit=5000"

        args = opentuner.default_argparser().parse_args()
        args.no_dups = True

        args.stop_after = gl.opentuner_parameter[0][1]
        # args.print_params = True


        GccFlagsTuner.main(args)


class RuntimeFrame(BaseFrame):

    def create_widgets(self):
        top = self.winfo_toplevel()
        self.menu_bar = tk.Menu()
        top['menu'] = self.menu_bar

        self.menu_bar.add_command(label = 'Set Spark',
                                  command = lambda: self.controller.show_frame(SparkPSFrame))
        self.menu_bar.add_command(label = 'Set Tasks',
                                  command = lambda: self.controller.show_frame(HibenchPSFrame))
        self.menu_bar.add_command(label = 'Parameter Space Summary',
                                  command = lambda: self.controller.show_frame(PSSummaryFrame))
        self.menu_bar.add_command(label = 'Runtime Monitor',
                                  command = lambda: self.controller.show_frame(RuntimeFrame))


        self.run_Result = tk.Button(self, text='Retrieve the Result', command=self.retrieve_Result_Summary)
        self.run_Result.grid(row=0, column=0, padx = 5, pady = 5, sticky = tk.W + tk.E)

    def retrieve_Result_Summary(self):
        # Example task ID table
        self.taskid_example = Label(self, text='Task1')
        self.taskid_example.grid(padx=5, pady=5, sticky=tk.W + tk.E)

        show_summary()

        self.task_summary = Label(self, text=gl.summary, anchor = 'w', justify=(LEFT))
        self.task_summary.grid(padx=5, pady=5, sticky=tk.W + tk.E)

        import os

        imgs = os.listdir('img')

        self.img = [PhotoImage(file="img/" + i) for i in imgs]
        self.canvas = Canvas(self, width=900, height=270)
        self.canvas.grid(padx=5, pady=5, sticky=tk.W + tk.E)
        for i in range(len(self.img)):
            self.canvas.create_image(160 + 300 * i, 150, image = self.img[i])

        import json
        json_result = ""
        with open('mmm_final_config.json') as json_data:
            json_result = json.load(json_data)
            json_data.close()

        print json_result
        json_result_string = "Result: \n"
        for k,v in json_result.iteritems():
            json_result_string += str(k) + " " + str(v) + "\n"
        # json_result.replace(',', '\n')
        # json_result = json_result[1:-1]
        self.best_parameter_summary = Label(self, text = json_result_string, anchor = 'w', justify=(LEFT))
        self.best_parameter_summary.grid(padx=5, pady=5, sticky=tk.W + tk.E)


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
        for f in (SparkPSFrame, HibenchPSFrame, PSSummaryFrame, RuntimeFrame):
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

