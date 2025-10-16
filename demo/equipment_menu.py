import tkinter as tk

# Window setup
root = tk.Tk()
root.title("Equipment Menu")

# Set windows size to 1080x1920
root.geometry("1080x1920")

# Define equipment options and their toggle states
toggle_vars = {
    "Barbell": tk.BooleanVar(value=False),
    "Dumbells": tk.BooleanVar(value=False),
    "Kettlebells": tk.BooleanVar(value=False),
    "Bench": tk.BooleanVar(value=False),
    "Rack": tk.BooleanVar(value=False),
}

# toggle function
def toggle(option):
    current = toggle_vars[option].get()
    toggle_vars[option].set(not current)
    update_button_style(option)
    print(f"{option} = {toggle_vars[option].get()}")

# Simple function to update button style based on state
def update_button_style(option):
    button = buttons[option]
    if toggle_vars[option].get():
        button.config(bg="lightgreen")
    else:
        button.config(bg="lightcoral")

# Create buttons
buttons = {}
for i, option in enumerate(toggle_vars):
    button = tk.Button(
        root,
        text=f"{option}",
        width=20,
        height=3,
        bg="lightcoral",
        font=("Arial", 20, "bold"),
        command=lambda opt=option: toggle(opt)
    )
    button.pack(pady=20)
    buttons[option] = button

# Run the app
root.mainloop()
