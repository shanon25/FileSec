from tkinter import *
from PyPDF2 import *
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import string
import time
from ctypes import windll
from backend import execute
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
    file = askopenfile(parent=root, mode='rb', title="Choose file",
                       filetypes=[("Word Document", "*.docx"), ("PDF file", "*.pdf")])

    if file:
        text.set("Click to Scan")

    else:
        text.set("Upload")
        messagebox.showerror("Error", "Please select a file!!!")
        file = askopenfile(parent=root, mode='rb', title="Choose file", filetypes=[("Word Document", "*.docx"), ("PDF file", "*.pdf")])


# button
text = StringVar()
button1 = Button(root, textvariable=text, text="Upload", command=lambda: Uploading(), font="Raleway", width=10, height=2, bg="light blue")
button1.place(x=260, y=310)
text.set("Upload")


#textbox


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

usb()

root.mainloop()
