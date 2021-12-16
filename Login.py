import tkinter as tk
from tkinter import LEFT

root = tk.Tk()

# Defining the size of the application
app = tk.Canvas(root.maxsize(width=500, height=400))
app = tk.Canvas(root.minsize(width=500, height=400))
app.grid(columnspan=4, rowspan=4)

# login entries and lables
Uname = tk.Label(root, text="Username:", font="Raleway", pady=20)
Uname.grid(row=1)
entry = tk.Entry(root, borderwidth=4)
entry.grid(column=2, row=1)

Pwd = tk.Label(root, text="Password:", font="Raleway")
Pwd.grid(row=2)
entry2 = tk.Entry(root, borderwidth=4)
entry2.grid(column=2, row=2)

# adding a button
button = tk.Button(root, text="login", height=1, width=8, bg="light blue")
button.grid(column=2, row=3)
root.mainloop()
