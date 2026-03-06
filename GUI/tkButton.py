"""
tkButton.py - Custom Tkinter Button Widget

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Implements a custom button widget extending Tkinter functionality with
    customizable appearance and behavior. Provides unified interface for button
    styling including background color, text color, border styling, and
    event handling.
    
    Key Features:
    - Customizable background and foreground colors
    - Configurable border styling (color and thickness)
    - Support for text labels with font customization
    - Flexible layout management (place, grid, grid_remove)
    - Event binding for click command execution
    - Configurable widget state (NORMAL, DISABLED)
"""

import tkinter as tk
from tkinter import *
from tkinter.constants import DISABLED, NORMAL


class Button():
    """
    Custom button widget providing enhanced styling options for Tkinter applications.
    """
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
        """
        Initialize custom button widget with specified styling and behavior.
        
        Parameters:
            root: Parent Tkinter widget
            width (int): Button width in pixels
            height (int): Button height in pixels
            text (str): Button label text
            bg (str): Background color
            fg (str): Text foreground color
            font (str): Text font specification
            command (callable): Function to execute on button click
            bordercolor (str): Border outline color
            bordersize (int): Border thickness in pixels
            highlightcolor (str): Highlight color for active state
            state: Button state (NORMAL or DISABLED)
        """
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
        """
        Execute button command callback function on click event.
        
        Parameters:
            event: Tkinter event object from button click
            
        Returns:
            None
        """
        if (self.command != None):
            self.command()
    
    def place(self,anchor="nw",relx=0,rely=0):
        """
        Position button using place geometry manager.
        
        Parameters:
            anchor (str): Anchor position (default 'nw' for northwest)
            relx (float): Relative x position
            rely (float): Relative y position
            
        Returns:
            None
        """
        self.button_frame.place(anchor=anchor,relx=relx,rely=rely)
    
    def grid(self,row,column,sticky,rowspan=1,columnspan=1,ipady=0):
        """
        Position button using grid geometry manager.
        
        Parameters:
            row (int): Grid row number
            column (int): Grid column number
            sticky (str): Sticky position specification
            rowspan (int): Number of rows to span
            columnspan (int): Number of columns to span
            ipady (int): Internal padding in pixels
            
        Returns:
            None
        """
        self.button_frame.grid(row=row,column=column,sticky=sticky,rowspan=rowspan,columnspan=columnspan, ipady=ipady)

    def grid_forget(self):
        """
        Hide button while preserving grid position information.
        
        Returns:
            None
        """
        self.button_frame.grid_forget()
    
    def grid_remove(self):
        """
        Remove button from grid layout temporarily.
        
        Returns:
            None
        """
        self.button_frame.grid_remove()

    def configurebg(self,width=width,height=height,text=text,bg=bg,fg=fg,font=font,command=command,bordercolor=bordercolor,bordersize=bordersize):
        """
        Update button appearance and styling properties.
        
        Parameters:
            width (int): Updated button width
            height (int): Updated button height
            text (str): Updated button label text
            bg (str): Updated background color
            fg (str): Updated foreground color
            font (str): Updated font specification
            command (callable): Updated click command
            bordercolor (str): Updated border color
            bordersize (int): Updated border thickness
            
        Returns:
            None
        """
        self.button_frame.configure(width=self.width,height=self.height,bg=bg)
        self.label.configure(text=self.text,bg=bg,width=self.width,height=self.height,fg=self.fg,font=self.font,highlightbackground=self.bordercolor,highlightthickness=self.bordersize)
        self.command = self.command

