import tkinter as tk

#text class
class MyText(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, background="lightblue", **kwargs) # Call the original tk.Text constructor
    
    def insert_workout(self):
        self.insert("end", "Here is your workout: \n") #title
        self.insert("end", "\n") #blank line print
        for i in range(1, 11):
            self.insert("end", f"Exercise {i}: blank\n")
        self.insert("end", "\n")
        
#Functions
toggled = False
def toggle():
    print("Button Clicked!")
    text.insert_workout() #displays workout text

# Create a window
root = tk.Tk()
root.title("SmartLift")

# Create the button
button = tk.Button(root, text="Generate Workout", command=toggle, width=15)
button.pack(pady=20)

# Create a Text widget
text = MyText(root, wrap="none", width=40, height=10)
text.pack(side="left", fill="both", expand=True)

# Create a vertical scrollbar
scrollbar = tk.Scrollbar(root, orient="vertical", command=text.yview)
scrollbar.pack(side="right", fill="y")
text.config(yscrollcommand=scrollbar.set) # Connect the Text widget to the scrollbar

#Run
root.mainloop()