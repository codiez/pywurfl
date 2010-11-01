#!/usr/bin/env python

"""
pywurfl Browser Example

Copyright 2004-2010, Armand Lynch <lyncha@users.sourceforge.net>

This code is free software; you can redistribute it and/or modify it under
the terms of the LGPL License.

This is a simple WURFL browser.
"""

import sys

from Tkinter import *
from tkMessageBox import showerror, showinfo

from wurfl import *
from pywurfl.exceptions import *
from pywurfl.algorithms import Tokenizer

try:
    from pywurfl.algorithms import JaroWinkler
    JAROWINKLER = True
    jsearch = JaroWinkler(accuracy=.85)
except ImportError:
    JAROWINKLER = False

tsearch = Tokenizer()

def get_info():

    ua = unicode(uaentry.get().strip())

    if type_var.get() == "User Agent":
        try:
            device = devices.select_ua(ua, actual_device_root=adr_var.get(),
                                       normalize=normalize_var.get(),
                                       search=get_algo())
        except DeviceNotFound:
            showerror('Error', "Device Not Found")
            return
        except ActualDeviceRootNotFound:
            showerror('Error', "Actual Device Root Not Found")
            return
    else:
        try:
            device = devices.select_id(ua)
        except DeviceNotFound:
            showerror('Error', "Device Not Found")
            return

    display_device_info(device)

def get_algo():
    if JAROWINKLER:
        if stype_var.get() == "Jaro-Winkler":
            return jsearch
    return tsearch

def follow_link(event):
    indx = infotext.index("@%d, %d" % (event.x, event.y))
    trange = infotext.tag_prevrange("link", indx)
    wid = unicode(infotext.get(trange[0], trange[1]))

    try:
        device = devices.select_id(wid)
    except DeviceNotFound:
        showerror('Error', "Device Not Found")
        return

    display_device_info(device)

def display_device_info(device):

    infotext.config(state=NORMAL)
    infotext.delete("1.0", END)
    infotext.insert(END, device)
    do_markup('User Agent', "meta")
    do_markup('WURFL ID', "meta")
    do_markup('Actual Device', "meta")
    do_markup("Fallbacks", "fallbacks")
    do_markup("True", "true")
    do_markup("False", "false")
    #remove_markup("       generic", "link", "+7c")
    #do_markup("       generic", "generic", "+7c")
    #do_group_markup()
    do_link_markup()
    infotext.config(state=DISABLED)

def do_markup(search, tag, tag_start="+0c"):
    start = "1.0"
    while 1:
        group_index = infotext.search(search, start, stopindex=END)
        if not group_index:
            break
        group_line = group_index.split('.')[0]
        infotext.tag_add(tag, group_index + tag_start, group_line + '.end')
        start = group_index + "+1c"

def do_group_markup():
    start = "1.0"
    while 1:
        group_index = infotext.search('--', start, stopindex=END)
        if not group_index:
            break
        group_line = group_index.split('.')[0]
        group_line = str(int(group_line) - 1)
        infotext.tag_add('group', group_line + ".0", group_line + '.end')
        start = group_index + "+1c"

def do_link_markup():
    start, finish = infotext.tag_ranges('fallbacks')
    f1, f2 = finish.split('.')
    f1 = int(f1)
    f2 = int(f2)

    toggle = True

    link_starts = []
    link_stops = []
    while 1:
        index = infotext.search("'", start, stopindex=END)
        if not index:
            break

        i1, i2 = index.split('.')
        i1 = int(i1)
        i2 = int(i2)

        if i1 <= f1 and i2 < f2:
            if toggle:
                link_starts.append(index + '+1c')
                toggle = False
            else:
                link_stops.append(index)
                toggle = True
            start = index + '+1c'
        else:
            break

    for lstart, lstop in zip(link_starts, link_stops):
        infotext.tag_add('link', lstart, lstop)


#def remove_markup(search, tag, tag_start="+0c"):
#    start = "1.0"
#    while 1:
#        group_index = infotext.search(search, start, stopindex=END)
#        if not group_index:
#            break
#        group_line = group_index.split('.')[0]
#        infotext.tag_remove(tag, group_index + tag_start, group_line + '.end')
#        start = group_index + "+1c"


def change_cursor(type="hand"):
    if type == "hand":
        infotext.config(cursor="hand1")
    else:
        infotext.config(cursor="arrow")


def printit(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def change_type():
    slabel.config(text=type_var.get())


def about_pywurfl():
    msg = "pywurfl Browser Example\nCopyright 2004-2006, Armand Lynch "
    msg += "<lyncha@users.sourceforge.net>\n\n"
    msg += "This code is free software; you can redistribute it and/or\n"
    msg += "modify it under the terms of the BSD License.\n"

    showinfo("About pywurfl Browser", msg)



root = Tk()
root.title("pywurfl Browser v5.1")

mroot = Menu(root)

mfile = Menu(mroot, tearoff=0)
mfile.add_command(label="Exit", command=root.quit)

type_var = StringVar()
stype_var = StringVar()
normalize_var = BooleanVar()
adr_var = BooleanVar()

type_var.set("User Agent")
if JAROWINKLER:
    stype_var.set("Jaro-Winkler")
else:
    stype_var.set("Tokenizer")
# normalize_noise
normalize_var.set(True)
# actual_device_root
adr_var.set(False)

soptions = Menu(mroot, tearoff=0)
soptions.add_radiobutton(label="User Agent", variable=type_var,
                         command=change_type)
soptions.add_radiobutton(label="WURFL ID", variable=type_var,
                         command=change_type)
soptions.add_separator()
soptions.add_checkbutton(label="Normalize User Agent", variable=normalize_var)
soptions.add_checkbutton(label="Actual Device", variable=adr_var)
if JAROWINKLER:
    soptions.add_separator()
    soptions.add_radiobutton(label="Jaro-Winkler", variable=stype_var)
    soptions.add_radiobutton(label="Tokenizer", variable=stype_var)

mabout = Menu(mroot, tearoff=0)
mabout.add_command(label="About", command=about_pywurfl)

mroot.add_cascade(label="File", menu=mfile)
mroot.add_cascade(label="Search Options", menu=soptions)
#mroot.add_cascade(label="Capability Display", menu=coptions)
mroot.add_cascade(label="Help", menu=mabout)

root.config(menu=mroot)

frm1 = Frame(root)
frm2 = Frame(root)

slabel = Label(frm1, text="User Agent", padx=5)

uaentry = Entry(frm1, bg="#fffff6", bd=1)
uaentry.bind("<Return>", lambda e: get_info())

infotext = Text(frm2, bg="#fffff6", height=40, width=80, relief=FLAT)
sbar = Scrollbar(frm2, bd=1, width=12)
sbar.config(command=infotext.yview)
infotext.config(yscrollcommand=sbar.set)

infotext.tag_config("group", borderwidth=1, foreground="#fdcd00",
                    font=("Helvetica", "11", "bold"))
infotext.tag_config("meta", borderwidth=1, foreground="#778899",
                    font=("Helvetica", "11", "bold"))
infotext.tag_config("fallbacks", borderwidth=1, foreground="#778899",
                    font=("Helvetica", "11", "bold"), wrap="word")
infotext.tag_config("false", foreground="red")
infotext.tag_config("true", foreground="darkgreen")
infotext.tag_config("link", foreground="blue", underline=1,
                    font=("Helvetica", "10", "bold"))
infotext.tag_config("generic", foreground="blue", underline=0)

infotext.tag_bind("link", "<Button-1>", lambda e: follow_link(e))
infotext.tag_bind("link", "<Enter>", lambda e: change_cursor("hand"))
infotext.tag_bind("link", "<Leave>", lambda e: change_cursor("arrow"))

infotext.config(cursor="arrow")
infotext.config(state=DISABLED)

frm1.pack(fill=X, anchor=W)
frm2.pack(expand=YES, fill=BOTH)
slabel.pack(side=LEFT)
uaentry.pack(side=LEFT, expand=YES, fill=X)
infotext.pack(side=LEFT, expand=YES, fill=BOTH)
sbar.pack(side=LEFT, fill=Y)

root.mainloop()
