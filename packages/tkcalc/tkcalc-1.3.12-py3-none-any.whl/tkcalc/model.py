#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  model.py
#
#  Copyright 2021 Elia Toselli l' hacker <elia@camillo-sparky>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

"""
This is the core of the tkinter calc. This code contains the definition of the buttons
and the function for managing the buffer.
"""

import math
import tkinter as tk
import tkinter.messagebox as tkm


class app:
    """
This is the core class. It defines a unique block that contains all the application.
    """
    def __init__(self):
        """This makes the window. It should not be called directly,
        unless you want to patch my application, with a subclass."""
        self.root = tk.Tk()
        self.root.title("Elia's Calculator")
        self.buffer = ""

    def add_cmd(self, cmd):
        """
This adds a command to the end of the buffer, and also to the end of the
text entry. You should call it only to manage manually the buffer,
and only if you know what you are doing.
The parameter 'self' is the 'app' object, and 'cmd' is the string you want
to insert.
        """
        self.buffer += str(cmd)
        self.bufw.insert(tk.END, str(cmd))

    def equal(self):
        """
It calculates the result. Don't call it, please! :)
        """
        try:
            res = eval(self.buffer)
            self.buffer = str(res)  # sostituisce al buffer il risultato
            self.bufw.delete(0, tk.END)
            self.bufw.insert(0, str(res))
        except (ZeroDivisionError, TypeError, ValueError, SyntaxError) as e:
            self.err.configure(text="ERROR: " + e.args[0])

    def quit(self):
        "It closes the app."
        self.root.destroy()

    def info(self):
        "It shows the 'about' window, in Italian."
        tkm.showinfo("About", """
Elia's Calculator 1.2.5
Copyright (C) 2021 Elia Toselli.

Il programma è sotto licenza GPL,
quindi potete copiarlo e redistribuirlo,
ma solo lasciando intatto il copyright.
        """)

    def inbuf(self, event):
        self.buffer = str(self.bufw.get())
        self.equal()

    def sqrt(self):
        try:
            self.equal()
            self.buffer = str(float(math.sqrt(float(self.buffer))))
            self.bufw.delete(0, tk.END)
            self.bufw.insert(0, self.buffer)
        except ValueError as e:  # noqa
            self.err.configure(text="ERROR: " + e.args[0])

    def clear(self):
        self.buffer = ""
        self.bufw.delete(0, tk.END)

    def draw_widgets(self):
        self.base_menu = tk.Menu(self.root)
        self.root.config(menu=self.base_menu)
        self.menu_file = tk.Menu(self.base_menu)
        self.base_menu.add_cascade(label="File", menu=self.menu_file)
        self.menu_file.add_command(label="Informazioni", command=self.info)
        self.menu_file.add_command(label="Esci", command=self.quit)
        self.bufw = tk.Entry(self.root)
        self.bufw.focus_set()
        self.bufw.bind("<Return>", self.inbuf)
        self.bufw.pack(side=tk.TOP, fill=tk.X)
        self.bdy = tk.Frame(self.root)
        self.err = tk.Label(self.bdy, text="No error occurred.")
        self.err.pack(side=tk.TOP, fill=tk.X)
        self.btns = tk.Frame(self.bdy)
        self.b0 = tk.Button(self.btns, text="  0  ", command=lambda: self.add_cmd('0')).grid(row=3,column=0) # noqa
        self.b1 = tk.Button(self.btns, text="  1  ", command=lambda: self.add_cmd('1')).grid(row=0,column=0) # noqa
        self.b2 = tk.Button(self.btns, text="  2  ", command=lambda: self.add_cmd('2')).grid(row=0,column=1) # noqa
        self.b3 = tk.Button(self.btns, text="  3  ", command=lambda: self.add_cmd('3')).grid(row=0,column=2) # noqa
        self.b4 = tk.Button(self.btns, text="  4  ", command=lambda: self.add_cmd('4')).grid(row=1,column=0) # noqa
        self.b5 = tk.Button(self.btns, text="  5  ", command=lambda: self.add_cmd('5')).grid(row=1,column=1) # noqa
        self.b6 = tk.Button(self.btns, text="  6  ", command=lambda: self.add_cmd('6')).grid(row=1,column=2) # noqa
        self.b7 = tk.Button(self.btns, text="  7  ", command=lambda: self.add_cmd('7')).grid(row=2,column=0) # noqa
        self.b8 = tk.Button(self.btns, text="  8  ", command=lambda: self.add_cmd('8')).grid(row=2,column=1) # noqa
        self.b9 = tk.Button(self.btns, text="  9  ", command=lambda: self.add_cmd('9')).grid(row=2,column=2) # noqa
        self.badd = tk.Button(self.btns, text="  +  ", command=lambda: self.add_cmd('+')).grid(row=4,column=0) # noqa
        self.bmin = tk.Button(self.btns, text="  -  ", command=lambda: self.add_cmd('-')).grid(row=4,column=1) # noqa
        self.bmul = tk.Button(self.btns, text="  *  ", command=lambda: self.add_cmd('*')).grid(row=5,column=0) # noqa
        self.bdiv = tk.Button(self.btns, text="  /  ", command=lambda: self.add_cmd('/')).grid(row=4,column=2) # noqa
        self.bdiv = tk.Button(self.btns, text="  ^  ", command=lambda: self.add_cmd('**')).grid(row=5,column=1) # noqa
        self.bsqrt = tk.Button(self.btns, text="SQRT", command=lambda: self.sqrt()).grid(row=5,column=2) # noqa
        self.beq = tk.Button(self.btns, text="  =  ", command=lambda: self.equal()).grid(row=6,column=0) # noqa
        self.bp1 = tk.Button(self.btns, text="  (  ", command=lambda: self.add_cmd("(")).grid(row=3,column=1) # noqa
        self.bp2 = tk.Button(self.btns, text="  )  ", command=lambda: self.add_cmd(")")).grid(row=3,column=2) # noqa
        self.bce = tk.Button(self.btns, text="  C  ", command=lambda: self.clear()).grid(row=6,column=2) # noqa
        self.btns.pack(side=tk.BOTTOM)
        self.bdy.pack(side=tk.BOTTOM)


if __name__ == "__main__":
    clc = app()
    clc.draw_widgets()
    clc.root.mainloop()
