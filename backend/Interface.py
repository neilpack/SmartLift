import tkinter as tk


def toggle():
    global toggled
    toggled = not toggled
    if toggled:
        print("YES")
        button.config(text="YES")
    else:
        print("NO")
        button.config(text="NO")

# Create a windows
root = tk.Tk()
root.title("Window")

toggled = False

# Create the button
button = tk.Button(root, text="Yes", command=toggle, width=15)
button.pack(pady=20)

# Start the GUI event loop
root.mainloop()