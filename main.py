from tkinter import *
from PyPDF2 import *
from tkinter.filedialog import askopenfile

root = Tk()

# Window size
app = root.maxsize(600, 900)
app = root.minsize(600, 900)

# label
label1 = Label(root, text="Upload a PDF or Word document to scan for Malware", font="Raleway")
label1.place(x=118, y=270)


# uploading function
def Uploading():
    text.set("Uploading...")
    file = askopenfile(parent=root, mode='rb', title="Choose file", filetypes=[("PDF file", "*.pdf")])

    if file:
        text.set("Click to Scan")
        text.set("Scanning...")

    else:
        text.set("No files were selected!")
        button2 = Button(root, textvariable=text, command=lambda: Uploading(), font="Raleway", width=18,
                         height=2, bg="light blue")
        button2.place(x=220, y=310)


# button
text = StringVar()
button1 = Button(root, textvariable=text, text="Upload", command=lambda: Uploading(), font="Raleway", width=10,
                 height=2, bg="light blue")
button1.place(x=260, y=310)
text.set("Upload")

root.mainloop()
