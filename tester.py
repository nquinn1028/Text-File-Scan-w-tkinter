# !/usr/bin/python3

from tkinter import *
from tkinter import filedialog
import re

# This junction is used only in the development of this program.
def gather_data():
    file_1 = openmodelfile('First')
    file_2 = openmodelfile('Second')
    Names_2 = []
    Data_2A = []
    Data_2B = []
    Names_1 = []
    Data_1B = []
    Data_1A = []
    with open(file_2) as file_in_2:
        for line in file_in_2:
            for ind in enumerate(file_in_2,0):
                split_2 = ind[1].split()
                Names_2.append(split_2[0])
                Data_2A.append(split_2[1])
                Data_2B.append(split_2[2])
    with open(file_1) as file_in_1:
        for line in file_in_1:
            for ind in enumerate(file_in_1,0):
                split_1 = ind[1].split()
                Names_1.append(split_1[0])
                Data_1B.append(split_1[1])
                Data_1A.append(split_1[2])
    return Names_2, Data_2A, Data_2B, Names_1, Data_1B, Data_1A

# The following functions and classes are to be retained for the final program.
def set_Project_Directory():
    root = Tk()
    root.withdraw()
    root.directory = filedialog.askdirectory(parent=root,title='Select a working directory')
    return root.directory

def openmodelfile(code):
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfile(parent=root,mode='r',title=f'Choose a {code} file')
    return filename.name

def find_index(item, list):
    index = []
    for ind in range(len(list)):
        if list[ind] == item:
            index = ind
    return index

class set_Project_Name():
    def __init__(self):
        self.root=Tk()
        self.root.title('Enter the Project Title')
        self.root.geometry('300x50')
        self.entry=Entry(self.root)
        self.entry.pack(fill=BOTH, expand=True)
        self.frame=Frame(self.root)
        self.frame.pack(anchor=CENTER)

        self.Ebutton = Button(self.frame, text="Enter", command=self.Return)
        self.Ebutton.pack(side=LEFT)
        self.Qbutton = Button(self.frame, text="Quit", command=self.root.quit)
        self.Qbutton.pack(side=LEFT)
        self.root.bind('<Return>', self.Return)

        self.root.mainloop()

    def Return(self, event=None):
        self.text=self.entry.get()
        self.root.destroy()

class set_Project_Params():
    def __init__(self):
        self.Master = Tk()
        self.Master.title('Enter the Structure Parameters')
        self.Master.geometry('768x500')
        self.container = Frame(self.Master)
        self.canvas = Canvas(self.container)
        self.vsb = Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        self.mainframe = Frame(self.canvas)

        self.mainframe.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.mainframe.bind('<Enter>', self._bound_to_mousewheel)
        self.mainframe.bind('<Leave>', self._unbound_to_mousewheel)

        self.canvas.create_window((0,0), window=self.mainframe, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.vsb.pack(side=RIGHT, fill=Y)

        self.col1 = Button(self.mainframe, text='Col1', width=20, command=None)
        self.col1.grid(row=0, column=0)
        self.col2 = Button(self.mainframe, text='Col2', width=20, command=None)
        self.col2.grid(row=0, column=1)
        self.col3 = Button(self.mainframe, text='Col3', width=20, command=None)
        self.col3.grid(row=0, column=2)
        self.col4 = Button(self.mainframe, text='Col4', width=20, command=None)
        self.col4.grid(row=0, column=3)
        self.col5 = Button(self.mainframe, text='Col5', width=20, command=None)
        self.col5.grid(row=0, column=4)

        self.col1_data = []
        self.col2_menu = []
        self.col2_text = []
        self.col2_select = []
        self.col3_data = []
        self.col3_text = []
        self.col4_entry = []
        self.col4_select = []
        self.col5_entry = []
        self.col5_select = []
        for index in range(len(Names_2)):
            self.col2_text.append(StringVar(self.mainframe))
            self.col2_text[index].set(Names_1[0])
            self.col3_text.append(StringVar(self.mainframe))
            self.col3_text[index].set('Data 1A: ' + self.getData1A(Names_1[0]) + '\n' +
                              'Data 1B: ' + self.getData1B(Names_1[0]) + '\n' +
                              'Data 2A: ' + self.getData2A(Names_2[index]) + '\n' +
                              'Data 2B: ' + self.getData2B(Names_2[index]))
            self.makeRow(index)

        self.bframe = Frame(self.Master)
        self.Cbutton = Button(self.bframe, text="Create Files", command=self.create_files)
        self.Cbutton.pack(side=LEFT)
        self.Qbutton = Button(self.bframe, text="Quit", command=self.Master.quit)
        self.Qbutton.pack(side=LEFT)
        self.bframe.pack(side=BOTTOM)
        self.Master.bind('<Return>', self.create_files)

        self.Master.mainloop()

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def makeRow(self, value):
        self.col1_data.append(Label(self.mainframe, text=Names_2[value]))
        self.col1_data[value].grid(row=value+1, column=0)
        self.col2_menu.append(OptionMenu(self.mainframe, self.col2_text[value], *Names_1, command=lambda new_value: self.displaydetails(new_value, self.col1_data[value].cget('text'), value)))
        self.col2_menu[value].grid(row=value+1, column=1)
        self.col3_data.append(Label(self.mainframe, textvariable=self.col3_text[value]))
        self.col3_data[value].grid(row=value+1, column=2)
        self.col4_entry.append(Entry(self.mainframe))
        self.col4_entry[value].grid(row=value+1, column=3)
        self.col5_entry.append(Entry(self.mainframe))
        self.col5_entry[value].grid(row=value+1, column=4)

    def displaydetails(self, name_1, hsname, rowvalue):
        self.col3_text[rowvalue].set('Data 1A: ' + self.getData1A(name_1) + '\n' +
                          'Data 1B: ' + self.getData1B(name_1) + '\n' +
                          'Data 2A: ' + self.getData2A(hsname) + '\n' +
                          'Data 2B: ' + self.getData2B(hsname))

    def getData1A(self, name_1):
        index = find_index(name_1, Names_1)
        return Data1A[index]

    def getData1B(self, name_1):
        index = find_index(name_1, Names_1)
        return Data1B[index]

    def getData2A(self, hsname):
        index = find_index(hsname, Names_2)
        return Data2A[index]

    def getData2B(self, hsname):
        index = find_index(hsname, Names_2)
        return Data2B[index]

    def create_files(self, event=None):
        for struct in range(len(Names_2)):
            self.col4_select.append(self.col4_entry[struct].get())
            self.col5_select.append(self.col5_entry[struct].get())
            self.col2_select.append(self.col2_text[struct].get())
        eval('self.Master.quit()')

class _exit_program():
    def __init__(self):
        self.root = Tk()
        self.notice = Label(self.root, text='Exiting the Program')
        self.notice.pack(side=TOP)
        self.OKbutton = Button(self.root, text='OK', command=self.root.quit)
        self.OKbutton.pack(side=BOTTOM)
        self.root.mainloop()

class _program_complete():
    def __init__(self):
        self.root = Tk()
        self.notice = Label(self.root, text='Program Complete.\nFile Generated.')
        self.notice.pack(side=TOP)
        self.OKbutton = Button(self.root, text='OK', command=self.root.quit)
        self.OKbutton.pack(side=BOTTOM)
        self.root.mainloop()

try:
    project_name = set_Project_Name().text
    outdir = set_Project_Directory()
    Names_2, Data2A, Data2B, Names_1, Data1B, Data1A = gather_data()
    project_params = set_Project_Params()
    Locs_2 = project_params.col4_select
    Oris_2 = project_params.col5_select
    Vols_2 = project_params.col2_select
    with open(outdir + '/' + project_name + '.in', 'w') as file_out:
        for line in range(len(Names_2)):
            file_out.write(f'{Names_2[line]} : {Data2A[line]} : {Data2B[line]} : {Vols_2[line]} : {Locs_2[line]} : {Oris_2[line]}\n')
    _program_complete()
except:
    _exit_program()
