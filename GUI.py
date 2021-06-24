import tkinter as tk
import tkinter.font as tkFont

class App:
    def change():
        print("changed")

    def __init__(self, root):
        #setting title
        root.title("2IC80 - Group 12")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        #Entry 1
        sv_entry1 = tk.StringVar()
        sv_entry1.set("Attacker IP")
        sv_entry1.trace("w", self.change)

        entry_1=tk.Entry(root, textvariable=sv_entry1)
        entry_1["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        entry_1["font"] = ft
        entry_1["fg"] = "#333333"
        entry_1["justify"] = "left"
        entry_1["text"] = "Attacker IP"
        entry_1.bind("<FocusIn>", lambda args: entry_1.delete('0', 'end'))
        entry_1.bind("<Key>", lambda args: print(entry_1.get()))
        entry_1.place(x=10,y=10,width=240,height=25)
        
        label_1=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        label_1["font"] = ft
        label_1["fg"] = "#333333"
        label_1["justify"] = "center"
        label_1["text"] = "Attacker IP address"
        label_1.place(x=240,y=10,width=150,height=25)

        #Entry 2
        sv_entry2 = tk.StringVar()
        sv_entry2.set("Attacker IP")
        sv_entry2.trace("w", self.change)

        entry_2=tk.Entry(root, textvariable=sv_entry2)
        entry_2["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        entry_2["font"] = ft
        entry_2["fg"] = "#333333"
        entry_2["justify"] = "left"
        entry_2["text"] = "Attacker MAC"
        entry_2.bind("<FocusIn>", lambda args: entry_2.delete('0', 'end'))
        entry_2.bind("<Key>", lambda args: print(entry_2.get()))
        entry_2.place(x=10,y=40,width=240,height=25)
        
        label_2=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        label_2["font"] = ft
        label_2["fg"] = "#333333"
        label_2["justify"] = "center"
        label_2["text"] = "Attacker MAC address"
        label_2.place(x=240,y=40,width=150,height=25)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
