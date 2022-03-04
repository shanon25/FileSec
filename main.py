from tkinter import *
import requests
from PyPDF2 import *
from tkinter import filedialog
from tkinter import messagebox
import string
import time
import backend
from backend import *
from ctypes import windll
import os
import asyncio

root = Tk()

# Window size
app = root.maxsize(600, 750)
app = root.minsize(600, 750)

# label
label1 = Label(root, text="Upload a PDF or Word document to scan for Malware", font="Raleway")
label1.place(x=118, y=270)


# uploading function
def Uploading():
    text.set("Uploading...")
    file = filedialog.askopenfilename(initialdir="/", title="Choose file",
                       filetypes=[("Word Document", "*.docx"), ("PDF file", "*.pdf")])
    # filename label
    file_lbl = Label(root, fg="black", bg="light blue")
    file_lbl.grid(row=3, column=1)
    file_lbl.configure(text="File: "+file)


    if file:
        #button 2 for send the selected file to Virus total
        text.set("Click to Scan")
        button2 = Button(root, textvariable=text, text="Upload", command=lambda: showresult(file), font="Raleway", width=10, height=2,
                         bg="light blue")
        button2.place(x=260, y=310)

    else:
        text.set("Upload")
        messagebox.showerror("Error", "Please select a file!!!")
        file = askopenfile(parent=root, mode='rb', title="Choose file", filetypes=[("Word Document", "*.docx"), ("PDF file", "*.pdf")])

def showresult(file):
    result = backend.execute(file)
    show_results_in_ui(result)


# button 1 for uploading a file
text = StringVar()
button1 = Button(root, textvariable=text, text="Upload", command=Uploading, font="Raleway", width=10, height=2, bg="light blue")
button1.place(x=260, y=310)
text.set("Upload")

def show_results_in_ui(data):
    sc = Toplevel()
    sc_verbose_lbl = Label(root, text=f"Message: {data.get('verbose_msg')}", font="Raleway", bg="light blue")
    sc_total_lbl = Label(root, text=f"Total: {data.get('total')}", font="Raleway", bg="light blue")
    sc_pos_lbl = Label(root, text=f"Positives: {data.get('positives')}", font="Raleway", bg="light blue")
    sc_date_lbl = Label(root, text=f"Scan date: {data.get('scan_date')}", font="Raleway", bg="light blue")
    sc_verbose_lbl.place(x=100, y=500)
    sc_total_lbl.place(x=150, y=550)
    sc_pos_lbl.place(x=200, y=600)
    sc_date_lbl.place(x=250, y=650)
    sc.maxsize(600, 700)
    sc.minsize(700, 500)

# Advanced scanning window
def adv_scan():
    adv = Toplevel()
    adv.maxsize(600, 900)
    adv.minsize(600, 900)
    adv.title("Advanced Scan")


# Menu
menu = Menu(root)
root.config(menu=menu)


# quit function
def quit_form():
    response = messagebox.askyesno("Error", "Do you want to Exit?")
    if response == 1:
        command = root.quit()
    else:
        command = root


# USB scanning function
def scan():
    pop = Toplevel()
    pop.title("USB scanner")
    pop.maxsize(600, 700)
    pop.minsize(700, 500)
    btn_scn = Button(pop, textvariable=text, text="Scan", font="Raleway", width=10, height=2, bg="light blue")
    btn_scn.place(x=300, y=130)
    text.set("Scan")


# Usb status
def status():
    devices = []
    record_deviceBit = windll.kernel32.GetLogicalDrives()
    for label in string.ascii_uppercase:  # The uppercase letters 'A-Z'
        if record_deviceBit & 1:
            devices.append(label)
        record_deviceBit >>= 1
    return devices


# USB plugin message box
def usb():
    txt = StringVar()
    res = messagebox.askyesno("USB Detected!!", "USB is detected please click YES to scan all the PDFs and Word Documents in the device")
    if res == 1:
        scan()
    else:
        error()


# error message box
def error():
    er = messagebox.askyesno("Are you sure?", "Do you want to terminate this process?")
    if er != 1:
        usb()


# menu items
scan_menu = Menu(menu)
menu.add_cascade(label="Scans", menu=scan_menu)
scan_menu.add_command(label="Advanced Scan", command=adv_scan)
scan_menu.add_separator()
scan_menu.add_command(label="Exit", command=quit_form)

# report generator menu
report_menu = Menu(menu)
menu.add_cascade(label="Reports", menu=report_menu)
report_menu.add_command(label="PDF Reports")
report_menu.add_command(label="Word Document")
report_menu.add_command(label="CSV")

# help and about menu
help_menu = Menu(menu)
menu.add_cascade(label="Info", menu=help_menu)
help_menu.add_command(label="Help")
help_menu.add_command(label="About FileSec")

#usb()

root.mainloop()