import tkinter as tk

# Run with "python first_try.py"

## Create the main window, root is the main window object
root = tk.Tk()
root.title("My First GUI") # Banner text
root.geometry("400x500") # Default size of the window


## Widget 1 - Label
# Parameters: 
#   Required: window object, text=<text to display> 
#   Optional: font=<font family, size, weight>, fg=<text color>, bg=<background color>
#   Unused Optional: anchor=<N, NE, E, SE, S, SW, W, NW, center>, etc.
label = tk.Label(root, text="Hello World!", font=("Arial", 14, "bold"), fg="red", bg="green") 

# "Pack" the label to add it to the window with simple stacking
# Label parameters can be adjusted at the same time. 
#   Other optional parameters: padx=<pixels of margin (x-axis) from 
#       widget to neighboring widgets>, pady=<pixels>
label.pack(padx=20, pady=10)


## Widget 2 - Button
# Define the function to call when the button is clicked
def on_click():
    print("Button pressed!") # Print to console

# Parameters:
#   Required: window object, text=<text to display>, command=<function to call>
#   Optional: similar to Label, also has state=<normal or disabled>
button = tk.Button(root, text="Click Me", command=on_click)
button.pack(pady=10)


## Widget 3 - Entry (Text Input)
# Parameters:
#   Required: window object, width=<number of characters to display>
#   Optional: similar to Label, also has show=<character to display instead of input>
entry = tk.Entry(root, width=30, show="*") # Password field
entry.pack(pady=10)

# Get the text later:
text = entry.get() # Won't work here because this line is called immediately


## Widget 4 - Text (Multi-line Text Input)
# Parameters:
#   Required: window object, height=<number of lines>, width=<number of characters>
#   Optional: similar to Label, also has wrap=<word or char>
text_box = tk.Text(root, height=5, width=40, wrap="word")
text_box.pack(pady=10)

# To insert text into the text box:
# Parameters:
#   Required: index=<line number>.<character number>, text=<text to insert>
text_box.insert("1.0", "Type here...")


## Widget 5 - Frame (Container for other widgets)
# Parameters:
#   Required: window object, bg=<background color>
#   Optional: relief=<raised, sunken, etc.>, borderwidth=<pixels of thickness>
frame = tk.Frame(root, bg="darkgray", relief="sunken", borderwidth=2)
frame.pack(pady=10)

# Add widgets to the frame using grid layout:
# Grid uses row and column positioning
tk.Label(frame, text="Inside the frame").grid(row=0, column=0, pady=5, padx=5)
tk.Button(frame, text="Button in frame").grid(row=0, column=1)


# Widget 6 - Canvas (Drawing area)
# Parameters:
#   Required: window object, width=<pixels>, height=<pixels>
canvas = tk.Canvas(root, width=200, height=150, bg="white")
canvas.pack(pady=10)

# Draw a line (coordinates are x1, y1, x2, y2)
canvas.create_line(10, 10, 190, 140, fill="black", width=2)

# Draw a rectangle
canvas.create_rectangle(50, 50, 150, 100, outline="blue")


# Start the main event loop
root.mainloop()