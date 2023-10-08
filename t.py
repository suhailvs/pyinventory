# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win=Tk()

# Set the size of the window
win.geometry("700x350")
win.title("Parent Window")

# Create a Toplevel window
top=Toplevel()
top.geometry('600x250')
top.title("Child Window")

# Place the toplevel window at the top
top.wm_transient(win)

win.mainloop()