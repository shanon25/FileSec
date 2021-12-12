import tkinter as tk
from PyPDF2 import *
from tkinter.filedialog import askopenfile

root = tk.Tk()
# Specifying the size of the window
app = tk.Canvas(root, width=600, height=300)
app.grid(columnspan=3, rowspan=1)

# label
label1 = tk.Label(root, text="Scan an Existing PDF file for malware below", font="Raleway")
label1.grid(columnspan=3, column=0, row=1)


# uploading files
def uploading():
    text.set("Loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("PDF file", "*.pdf")])
    text.set("Scanning..")


# files uploading option
text = tk.StringVar()
button = tk.Button(root, textvariable=text, command=lambda: uploading(), font="Raleway", bg="light blue", height=2,
                   width=10)
text.set("Upload")
button.grid(column=1, row=2)

app = tk.Canvas(root, width=600, height=250)
app.grid(columnspan=3)

root.mainloop()
