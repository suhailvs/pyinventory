#! /usr/bin/python3

#import sys
#if len(sys.argv)==2:    
#    if sys.argv[1] == 'create_tables': 
import models
from forms import home 

models.create_tables_if_not_exist()
root=home.Tk()
root['bg']='black'
root.resizable(0,0)
frmmenu=home.FormMenu(root)
root.mainloop()