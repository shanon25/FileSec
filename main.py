from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import string
import threading
import time
from tkinter.filedialog import askopenfile
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
label1.place(x=100, y=150)


# uploading function
def Uploading():
    text.set("Uploading...")
    file = filedialog.askopenfilename(initialdir="/", title="Choose file",
                                      filetypes=[("Word Document", "*.docx"), ("PDF file", "*.pdf")])
    # filename label
    file_lbl = Label(root, fg="black")
    file_lbl.place(x=90, y=280)
    file_lbl.configure(text="File: " + file)

    if file:
        # button 2 for send the selected file to Virus total
        text.set("Click to Scan")
        button2 = Button(root, textvariable=text, text="Upload", command=lambda: showresult(file), font="Raleway",
                         width=10, height=2,
                         bg="light blue")
        button2.place(x=260, y=200)

    else:
        text.set("Upload")
        messagebox.showerror("Error", "Please select a file!!!")
        file = askopenfile(parent=root, mode='rb', title="Choose file",
                           filetypes=[("Word Document", "*.docx"), ("PDF file", "*.pdf")])


def showresult(file):
    result = backend.execute(file)
    show_results_in_ui(result)


# button 1 for uploading a file
text = StringVar()
button1 = Button(root, textvariable=text, text="Upload", command=Uploading, font="Raleway", width=10, height=2,
                 bg="light blue")
button1.place(x=260, y=200)
text.set("Upload")


def show_results_in_ui(data):
    sc_verbose_lbl = Label(root, text=f"Message: {data.get('verbose_msg')}", font="Raleway", bg="light green",
                           fg="black")
    sc_total_lbl = Label(root, text=f"Total: {data.get('total')}", font="Raleway", bg="light green", fg="black")
    sc_pos_lbl = Label(root, text=f"Positives: {data.get('positives')}", font="Raleway", bg="light green",
                       fg="black")
    sc_date_lbl = Label(root, text=f"Scan date: {data.get('scan_date')}", font="Raleway", bg="light green",
                        fg="black")
    sc_verbose_lbl.place(x=90, y=350)
    sc_total_lbl.place(x=90, y=400)
    sc_pos_lbl.place(x=90, y=450)
    sc_date_lbl.place(x=90, y=500)

    if data.get('positives'):
        sc_mal_lbl = Label(root, text="MALWARE DETECTED!!!", bg="brown", fg="white")
        sc_mal_lbl.place(x=140, y=550)
    else:
        sc_mal_lbl = Label(root, text="NO MALWARE IS DETECTED, FILE IS SAFE", bg="light green", fg="black",
                           font="Raleway")
        sc_mal_lbl.place(x=140, y=550)


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
text2 = StringVar()
text3 = StringVar()


def scan():
    pop_global = Toplevel()
    pop_global.title("USB scanner")
    pop_global.maxsize(700, 500)
    pop_global.minsize(700, 500)
    file_txt = Listbox(pop_global, width=90, height=20)
    file_txt.place(x=80, y=160)
    btn_scn = Button(pop_global, textvariable=text2, text="List the files", command=lambda: Filetype(pop_global),
                     font="Raleway",
                     width=10, height=2, bg="brown", fg="white")
    btn_scn.place(x=300, y=50)
    text2.set("Scan the files")
    btn1_scn = Button(pop_global, textvariable=text3, text="Scan", font="Raleway", width=10, height=2, bg="brown",
                      fg="white")
    text3.set("Scan")


# Usb status
def status():
    devices = []
    record_deviceBit = windll.kernel32.GetLogicalDrives()
    for label in string.ascii_uppercase:  # The uppercase letters 'A-Z'
        if record_deviceBit & 1:
            devices.append(label)
        record_deviceBit >>= 1
    return devices


def detect_device():
    global dirname
    while True:
        original = set(status())
        print('Detecting...')
        time.sleep(1)
        add_device = set(status()) - original
        subt_device = original - set(status())

        if len(add_device):
            print("There were %d" % (len(add_device)))
            for drive in add_device:
                print("The drives added: %s." % drive)
            dirname = f'{drive}:\\'
            usb()

        elif len(subt_device):
            print("There were %d" % (len(subt_device)))
            for drive in subt_device:
                print("The drives remove: %s." % drive)


# Listing down PDF and word files in an external drive
def Filetype(pop):
    print(dirname)
    # device = detect_device()
    file_txt = Listbox(pop, width=90, height=20)
    file_txt.place(x=80, y=160)
    file_txt.delete(0, END)
    filenames = {}
    ext = ('.pdf', '.docx')
    for root, dirs, files in os.walk(dirname):
        for index, file in enumerate(files):
            if file.endswith(ext):
                filenames[file] = f"{root}{file}"
                file_txt.insert(index, file)
    counter = 0
    for fname, fpath in filenames.items():
        result = backend.execute(fpath)
        positive_msg = "Couldn't verified"

        if result:
            if result.get('positives'):
                positive_msg = "MALWARE DETECTED!!!"

            else:
                positive_msg = "NO MALWARE IS DETECTED, FILE IS SAFE"

        label_text = f"{fname} - {positive_msg}"
        file_txt.delete(counter)
        file_txt.insert(counter, label_text)
        counter += 1


# USB plugin message box
def usb():
    device = status()
    res = messagebox.askyesno("USB Detected!!",
                              "USB is detected please click YES to scan all the PDFs and Word Documents in the device")
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


class RunFunctionInBackground(threading.Thread):

    def __init__(self, function, *args, **kwargs):
        threading.Thread.__init__(self)
        self.runnable = function
        self.daemon = True
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.runnable(*self.args, **self.kwargs)


thread = RunFunctionInBackground(detect_device)
thread.start()

root.mainloop()
