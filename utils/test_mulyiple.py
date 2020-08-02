import tkinter as tk

result = ['Weekly', 'Monthly', 'Annual']

class Application(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.listbox = dict() # lower case for variable name 
        self.label = dict() # lower case for variable name 

        for inst in result:
            #textenter = "Select the required output format" + inst
            textenter = inst

            self.label[inst] = tk.Label(self, text=textenter)
            self.label[inst].grid(columnspan=2, sticky=tk.W)

            self.listbox[inst] = tk.Listbox(self, selectmode=tk.MULTIPLE, exportselection=0)
            self.listbox[inst].grid(sticky=tk.W)

            for items in ["Text", "XML", "HTML"]:
                self.listbox[inst].insert(tk.END,items)

        self.submit_button = tk.Button(self, text="Submit", command=self.returns)
        self.submit_button.grid(row=7, column=1, sticky=tk.W)


    def returns(self):
        self.content = []

        for inst in result:
            self.content.append(self.listbox[inst].curselection())

        print (self.content)

        self.master.destroy()    


root = tk.Tk()
app = Application(root)
root.title("Output Formats")
app.mainloop()