import tkinter as tk
from tkinter import *
from tkinter.constants import DISABLED, NORMAL


class Button():
    button_frame = None
    root = None
    width=100
    height=20
    text=""
    bg="white"
    fg="black"
    font="f 12"
    bordercolor = "black"
    bordersize = 3
    label = None
    command = None
    state = tk.NORMAL

    def __init__(self,root,width=100,height=20,text="",bg="white",fg="black",font="f 12",command=None,bordercolor="black",bordersize=0,highlightcolor = "grey",state=DISABLED):
        self.root = root
        self.width=width
        self.height=height
        self.text=text
        self.bg=bg
        self.fg=fg
        self.font=font
        self.highlightcolor = highlightcolor
        self.command = command
        self.bordercolor = bordercolor
        self.bordersize = bordersize
        self.state = state
        self.button_frame = tk.Frame(root,width=width,height=height,bg=bg)
        self.label = tk.Label(self.button_frame,text=self.text,bg=self.bg,width=self.width,height=self.height,fg=self.fg,font=self.font,highlightbackground=self.bordercolor,highlightthickness=self.bordersize)
        self.label.place(anchor="center",relx=0.5,rely=0.5,relheight=1,relwidth=1)
        self.label.bind("<Button-1>",self.call_command)

    def call_command(self,event):
        if (self.command != None):
            self.command()
    
    def place(self,anchor="nw",relx=0,rely=0):
        self.button_frame.place(anchor=anchor,relx=relx,rely=rely)
    
    def grid(self,row,column,sticky,rowspan=1,columnspan=1,ipady=0):
        self.button_frame.grid(row=row,column=column,sticky=sticky,rowspan=rowspan,columnspan=columnspan, ipady=ipady)

    def grid_forget(self):
        self.button_frame.grid_forget()
    
    def grid_remove(self):
        self.button_frame.grid_remove()

    def configurebg(self,width=width,height=height,text=text,bg=bg,fg=fg,font=font,command=command,bordercolor=bordercolor,bordersize=bordersize):
        self.button_frame.configure(width=self.width,height=self.height,bg=bg)
        self.label.configure(text=self.text,bg=bg,width=self.width,height=self.height,fg=self.fg,font=self.font,highlightbackground=self.bordercolor,highlightthickness=self.bordersize)
        self.command = self.command

