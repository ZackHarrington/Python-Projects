import tkinter as tk
# ttk is integrated with the OS theme to be more aesthetically pleasing
from tkinter import ttk
import random
import time

## Create the main window
root = tk.Tk()
root.title("Snowman Generator")
root.geometry("1000x600")

# Snowflake animation variables
snowflakes = []
animation_id = None
elapsed_time = 0

# Global constants
WIND_TOP_SPEED = 10  # Maximum wind speed for slider
ZOOM_MAX = 100  # Maximum zoom level for slider
ZOOM_MIN = 1    # Minimum zoom level for slider
HEIGHT_MAX = 20  # Maximum snowman height (number of snowballs)
SIZE_DIFF_MAX = 1.5  # Maximum size difference multiplier
SIZE_DIFF_MIN = 0.5  # Minimum size difference multiplier


# ==================== MAIN LAYOUT ====================

# Create main container frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create left settings panel with scrollbar (1/3 width)
settings_outer_frame = ttk.Frame(main_frame, width=333)
settings_outer_frame.pack_propagate(False)  # Prevent frame from expanding based on child widgets
settings_outer_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=10, pady=10)

# Configure grid for the outer frame (2 columns: canvas and scrollbar)
settings_outer_frame.grid_rowconfigure(0, weight=1)
settings_outer_frame.grid_columnconfigure(0, weight=1)  # Canvas takes available space

# To support scrolling, it's easiest to use a Canvas widget
# highlightthickness=0 removes the border around the canvas
settings_canvas = tk.Canvas(settings_outer_frame, highlightthickness=0)
# Create the scrollbar and connect it to the canvas
scrollbar = ttk.Scrollbar(settings_outer_frame, orient="vertical", command=settings_canvas.yview)
# Create the actual frame that will hold all settings (placed inside the canvas)
settings_frame = ttk.Frame(settings_canvas)
# Connect the canvas scrolling area to the size of the inner frame (can change dynamically)
settings_frame.bind(
    "<Configure>",
    lambda e: settings_canvas.configure(scrollregion=settings_canvas.bbox("all"))
)
# Add the inner frame to the canvas (only supported through a window object)
settings_canvas_window = settings_canvas.create_window((0, 0), window=settings_frame, anchor="nw")
# Make the scrollbar visually reflect the current scroll position
settings_canvas.configure(yscrollcommand=scrollbar.set)
# Link the canvas width and frame width via the window
def _on_canvas_configure(event):
    settings_canvas.itemconfig(settings_canvas_window, width=event.width)
settings_canvas.bind("<Configure>", _on_canvas_configure)
# Use grid to place canvas and scrollbar side-by-side with precise control
settings_canvas.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
scrollbar.grid(row=0, column=1, sticky="ns", padx=10, pady=0)

# Create right canvas area (2/3 width)
canvas_frame = ttk.Frame(main_frame)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# === need to figure out why the settings panel will not match the defined width ===
# ************ also need to figure out coloring of the ttk widgets ************

# ==================== SETTINGS PANEL ====================

# Style configuration for better appearance
style = ttk.Style()
style.configure('Settings.TFrame', background='lightgray')

## Background Options Section
# Section title
bg_label = ttk.Label(settings_frame, text="Background Options", font=("Arial", 12, "bold"))
bg_label.pack(anchor=tk.CENTER, pady=(0, 5))

# Settings box for background options
bg_box = ttk.LabelFrame(settings_frame, padding=10)
bg_box.pack(fill=tk.X, pady=(0, 10))

# Background Color Dropdown
bg_color_frame = ttk.Frame(bg_box)
bg_color_frame.pack(fill=tk.X, pady=5)
ttk.Label(bg_color_frame, text="Color:").pack(side=tk.LEFT)
bg_color_var = tk.StringVar(value="light blue")
bg_color_combo = ttk.Combobox(bg_color_frame, textvariable=bg_color_var, 
                               values=["light blue", "white", "light gray", "green"], 
                               state="readonly", width=15)
bg_color_combo.pack(side=tk.LEFT, padx=5)

# Snow Checkbox (collapsible menu)
snow_var = tk.BooleanVar(value=True)
snow_check = ttk.Checkbutton(bg_box, text="Snow", variable=snow_var)
snow_check.pack(anchor=tk.W, pady=5)

# Snow options (collapsible submenu)
snow_options_frame = ttk.Frame(bg_box)
snow_options_frame.pack(anchor=tk.W, padx=20, fill=tk.X)

# Intensity Slider
intensity_frame = ttk.Frame(snow_options_frame)
intensity_frame.pack(fill=tk.X, pady=5)
ttk.Label(intensity_frame, text="Intensity:", width=10).pack(side=tk.LEFT)
intensity_var = tk.DoubleVar(value=0)
intensity_labels = {0: "Light", 1: "Medium", 2: "Heavy", 3: "Blizzard"}
intensity_slider = ttk.Scale(intensity_frame, from_=0, to=3, orient=tk.HORIZONTAL, variable=intensity_var)
intensity_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
intensity_value_label = ttk.Label(intensity_frame, text="Light", width=8)
intensity_value_label.pack(side=tk.LEFT, padx=5)
intensity_slider.config(state=tk.NORMAL)

# Wind Slider
wind_frame = ttk.Frame(snow_options_frame)
wind_frame.pack(fill=tk.X, pady=5)
ttk.Label(wind_frame, text="Wind:", width=10).pack(side=tk.LEFT)
wind_var = tk.DoubleVar(value=0)
wind_slider = ttk.Scale(wind_frame, from_=-WIND_TOP_SPEED, to=WIND_TOP_SPEED, 
                        orient=tk.HORIZONTAL, variable=wind_var)
wind_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
wind_value_label = ttk.Label(wind_frame, text="Calm", width=8)
wind_value_label.pack(side=tk.LEFT, padx=5)
wind_slider.config(state=tk.NORMAL)

# Zoom Slider
zoom_frame = ttk.Frame(bg_box)
zoom_frame.pack(fill=tk.X, pady=5)
ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT)
radius_var = tk.IntVar(value= (ZOOM_MAX-ZOOM_MIN) // 2)
zoom_slider = ttk.Scale(zoom_frame, from_=ZOOM_MIN, to=ZOOM_MAX, 
                        orient=tk.HORIZONTAL, variable=radius_var)
zoom_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


## Snowman Options Section
# Section title
sm_label = ttk.Label(settings_frame, text="Snowman Options", font=("Arial", 12, "bold"))
sm_label.pack(anchor=tk.CENTER, pady=(15, 5))

# Settings box for snowman options
sm_box = ttk.LabelFrame(settings_frame, padding=10)
sm_box.pack(fill=tk.X, expand=False)

# Height Slider
height_frame = ttk.Frame(sm_box)
height_frame.pack(fill=tk.X, pady=5)
ttk.Label(height_frame, text="Snowballs:").pack(side=tk.LEFT)
height_var = tk.IntVar(value=3)
height_slider = ttk.Scale(height_frame, from_=0, to=HEIGHT_MAX, 
                          orient=tk.HORIZONTAL, variable=height_var)
height_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
# Use fixed width to prevent canvas resizing
height_value_label = ttk.Label(height_frame, text=str(height_var.get()), width=2)
height_value_label.pack(side=tk.LEFT, padx=5)

# Size Difference Slider
size_diff_frame = ttk.Frame(sm_box)
size_diff_frame.pack(fill=tk.X, pady=5)
ttk.Label(size_diff_frame, text="Size Difference:").pack(side=tk.LEFT)
size_diff_var = tk.DoubleVar(value=(SIZE_DIFF_MAX-SIZE_DIFF_MIN)*0.85)
size_diff_slider = ttk.Scale(size_diff_frame, from_=SIZE_DIFF_MIN, to=SIZE_DIFF_MAX, 
                             orient=tk.HORIZONTAL, variable=size_diff_var)
size_diff_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
size_diff_value_label = ttk.Label(size_diff_frame, text="Equal", width=8)
size_diff_value_label.pack(side=tk.LEFT, padx=5)

# Hat Checkbox
hat_var = tk.BooleanVar(value=True)
hat_check = ttk.Checkbutton(sm_box, text="Hat", variable=hat_var)
hat_check.pack(anchor=tk.W, pady=3)

# Eyes Checkbox
eyes_var = tk.BooleanVar(value=True)
eyes_check = ttk.Checkbutton(sm_box, text="Eyes", variable=eyes_var)
eyes_check.pack(anchor=tk.W, pady=3)

# Carrot Nose Checkbox
carrot_var = tk.BooleanVar(value=True)
carrot_check = ttk.Checkbutton(sm_box, text="Carrot Nose", variable=carrot_var)
carrot_check.pack(anchor=tk.W, pady=3)

# Arms Checkbox
arms_var = tk.BooleanVar(value=True)
arms_check = ttk.Checkbutton(sm_box, text="Arms", variable=arms_var)
arms_check.pack(anchor=tk.W, pady=3)

# Buttons Checkbox
buttons_var = tk.BooleanVar(value=True)
buttons_check = ttk.Checkbutton(sm_box, text="Buttons", variable=buttons_var)
buttons_check.pack(anchor=tk.W, pady=3)

# Scarf Checkbox
scarf_var = tk.BooleanVar(value=False)
scarf_check = ttk.Checkbutton(sm_box, text="Scarf", variable=scarf_var)
scarf_check.pack(anchor=tk.W, pady=3)

# ==================== CANVAS ====================

# Create canvas for drawing
canvas = tk.Canvas(canvas_frame, bg=bg_color_var.get(), relief=tk.SUNKEN, bd=2)
canvas.pack(fill=tk.BOTH, expand=True)

# ==================== BOTTOM BAR ====================

# Create bottom bar frame (fixed at bottom, takes precedence)
bottom_bar = ttk.Frame(root, height=30)
bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
bottom_bar.pack_propagate(False)  # Prevent frame from shrinking

# Add separator line
separator = ttk.Separator(bottom_bar, orient='horizontal')
separator.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

# Configure grid for bottom_bar (3 columns: left, center, right)
bottom_bar.columnconfigure(0, weight=1)  # Left column
bottom_bar.columnconfigure(1, weight=1)  # Center column
bottom_bar.columnconfigure(2, weight=1)  # Right column

# Add Statistics checkbox to bottom bar (LEFT)
statistics_var = tk.BooleanVar(value=False)
statistic_check = ttk.Checkbutton(bottom_bar, text="Statistics", variable=statistics_var)
statistic_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Add random fun fact label to bottom bar (CENTER)
fun_facts = [
    "Snowmen can be built in various shapes and sizes!",
    "The largest snowman ever built was over 122 feet tall!",
    "Snowmen are often associated with winter holidays around the world.",
    "The tradition of building snowmen dates back to at least the Middle Ages.",
    "Snowmen can be decorated with anything from carrots to scarves!"
]
fun_fact_label = ttk.Label(bottom_bar, text=random.choice(fun_facts))
fun_fact_label.grid(row=0, column=1, padx=5, pady=5)

# Add a randomize button (RIGHT)
randomize_button = ttk.Button(bottom_bar, text="Randomize")
randomize_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

# ==================== UPDATE FUNCTIONS ====================

# Enable mousewheel scrolling
def _on_mousewheel(event):
    # event.delta is positive when scrolling up, negative when scrolling down
    # Divide by 120 to normalize mouse wheel events, multiply by -1 to invert direction
    settings_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
settings_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Update intensity slider label
def update_intensity_label(val):
    intensity_value_label.config(text=intensity_labels[int(float(val))])
intensity_slider.config(command=update_intensity_label)

# Update wind slider label
def update_wind_label(val):
    if float(val) > 1:
        wind_value_label.config(text="Easterly")
    elif float(val) < -1:
        wind_value_label.config(text="Westerly")
    else:
        wind_value_label.config(text="Calm")
wind_slider.config(command=update_wind_label)

# Update background color on change
# Need to accept *args to handle the event, don't need to use it
def update_bg_color(*args):
    canvas.config(bg=bg_color_var.get())
# Comboboxes dont have a command attribute, need to use the bind method for this
bg_color_combo.bind("<<ComboboxSelected>>", update_bg_color) 

# Draw snowman
def draw_snowman():
    last_radius = radius_var.get()
    last_y = canvas.winfo_height() - last_radius * 4/5 # Start position for the bottom snowball
    arm_snowball = height_var.get() * 3 // 5  # Middle snowball for arms
    for i in range(height_var.get()):
        radius = last_radius * size_diff_var.get()  # Decrease radius for higher segments
        x = canvas.winfo_width() // 2
        y = last_y - (last_radius + radius) * 2/3  # Stack segments vertically
        
        # Arms first so they appear in the snowball
        if arms_var.get() and i == arm_snowball:
            arm_x_offset = radius * 0.8
            arm_length = radius * 1.5
            arm_y_offset = radius * 0.2
            # Left arm
            canvas.create_line(x - arm_x_offset, y - arm_y_offset,
                            x - arm_x_offset - arm_length, y - arm_y_offset - arm_length / 2,
                            fill="saddle brown", width=radius * 0.1)
            # Right arm
            canvas.create_line(x + arm_x_offset, y - arm_y_offset,
                            x + arm_x_offset + arm_length, y - arm_y_offset - arm_length / 2,
                            fill="saddle brown", width=radius * 0.1)
        
        # Draw snowballs
        canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="white", outline="white"
        )
        last_y = y
        last_radius = radius

        if i == height_var.get() - 1:
            # Eyes
            if eyes_var.get():
                eye_offset_x = radius * 0.3
                eye_offset_y = radius * 0.2
                eye_size = radius * 0.1
                # Left eye
                canvas.create_oval(x - eye_offset_x - eye_size, y - eye_offset_y - eye_size,
                                x - eye_offset_x + eye_size, y - eye_offset_y + eye_size,
                                fill="black", outline="black")
                # Right eye
                canvas.create_oval(x + eye_offset_x - eye_size, y - eye_offset_y - eye_size,
                                x + eye_offset_x + eye_size, y - eye_offset_y + eye_size,
                                fill="black", outline="black")
            # Carrot Nose
            if carrot_var.get():
                nose_length = radius * 0.4
                nose_width = radius * 0.2
                canvas.create_polygon(x, y + nose_width / 2,
                                    x, y + nose_width * 3/2,
                                    x + nose_length, y + nose_width,
                                    fill="orange", outline="orange")
            # Hat
            if hat_var.get():
                hat_height = radius * 1.2
                hat_width = radius * 1.6
                brim_height = radius * 0.2
                # Brim
                canvas.create_rectangle(x - hat_width / 2, y - radius*4/5 - brim_height,
                                    x + hat_width / 2, y - radius*4/5,
                                    fill="black", outline="black")
                # Top hat
                canvas.create_rectangle(x - hat_width / 3, y - radius*4/5 - hat_height,
                                    x + hat_width / 3, y - radius*4/5,
                                    fill="black", outline="black")
            # Scarf
            if scarf_var.get():
                scarf_tail_length = radius * 0.5
                canvas.create_arc(x - radius*0.9, y + radius*0.2,
                                x + radius*0.9, y + radius,
                                start=0, extent=-180,
                                style="arc", outline="red", width=radius*0.2)
                canvas.create_polygon(x + radius*0.7, y + radius*0.9,
                                    x + radius*0.9, y + radius*0.8,
                                    x + radius*0.8, y + radius*0.9 + scarf_tail_length,
                                    x + radius*0.6, y + radius*0.8 + scarf_tail_length,
                                    fill="red", outline="red")

        # Buttons (two per middle snowball)
        if buttons_var.get() and 0 < i < height_var.get() - 1:
            for j in range(2):
                button_y = y - radius*0.05 + j * (radius*3/5)
                canvas.create_oval(x - radius/10, button_y - radius/10,
                                x + radius/10, button_y + radius/10,
                                fill="black", outline="black")

# Clear and redraw canvas
def redraw_canvas(*args):
    canvas.delete("all")
    
    # Background
    canvas.config(bg=bg_color_var.get())
    # draw traingular ground
    bottom_radius = radius_var.get()
    canvas.create_polygon(0, canvas.winfo_height(), # bottom left
                        canvas.winfo_width(), canvas.winfo_height(), # bottom right
                        canvas.winfo_width(), canvas.winfo_height() - bottom_radius*3/2, # top right
                        canvas.winfo_width()*4/5, canvas.winfo_height() - bottom_radius*2, # middle
                        0, canvas.winfo_height() - bottom_radius, # top left
                        fill="white", outline="white")

    # Snowman
    draw_snowman()

    # Snowflakes
    if snow_var.get():
        for snowflake in snowflakes:
            x, y = snowflake['x'], snowflake['y']
            size = snowflake['size']
            canvas.create_oval(x-size, y-size, x+size, y+size, fill="white", outline="white")
    
    # Statistics
    if statistics_var.get():
        canvas.create_text(10, 10, anchor="nw", 
                        text=f"Update time: {elapsed_time} ms")
        canvas.create_text(10, 30, anchor="nw", 
                        text=f"Snowflakes: {len(snowflakes)}")
        canvas.create_text(10, 50, anchor="nw", 
                        text=f"Intensity: {intensity_var.get():.1f}")
        canvas.create_text(10, 70, anchor="nw", 
                        text=f"Wind: {wind_var.get():.1f}")
        canvas.create_text(10, 90, anchor="nw", 
                        text=f"Zoom: {radius_var.get()}")
        canvas.create_text(10, 110, anchor="nw", 
                        text=f"Size Multiplier: {size_diff_var.get()}")

statistic_check.config(command=redraw_canvas)

# Update height slider label
def update_height_label(val):
    # val is a string that contains a float, but needs to be converted to an int for display
    height_value_label.config(text=str(int(float(val))))
    redraw_canvas()

# Update size difference slider label
def update_size_diff_label(val):
    if float(val) > 1:
        size_diff_value_label.config(text="Larger")
    elif float(val) < 1:
        size_diff_value_label.config(text="Smaller")
    else:
        size_diff_value_label.config(text="Equal")
    redraw_canvas()
size_diff_slider.config(command=update_size_diff_label)
height_slider.config(command=update_height_label)
zoom_slider.config(command=redraw_canvas)
hat_check.config(command=redraw_canvas)
eyes_check.config(command=redraw_canvas)
carrot_check.config(command=redraw_canvas)
arms_check.config(command=redraw_canvas)
buttons_check.config(command=redraw_canvas)
scarf_check.config(command=redraw_canvas)


# Animation function for snowflakes
def animate_snow():
    global snowflakes, animation_id, elapsed_time

    # Implement dynaimic frame timing
    frame_start = time.time()  # Record when frame started
    target_fps = 30
    target_frame_time = 1000 / target_fps # milliseconds

    if snow_var.get():
        # Animate snowflakes
        # Remove old snowflakes that are off-screen
        # Shorthand for generating a new list from an existing one with a condition
        snowflakes = [s for s in snowflakes if s['y'] < canvas.winfo_height() 
                      and -(canvas.winfo_height()*0.5) <= s['x'] <= canvas.winfo_width() 
                      + canvas.winfo_height()*0.5]

        # Add new snowflakes randomly based on intensity (More intensity = more snowflakes)
        if random.random() < (0.25 * (1 + intensity_var.get())):    
            snowflakes.append({
                'x': random.randint(int(-(canvas.winfo_height()*0.75)), 
                                    int(canvas.winfo_width() + canvas.winfo_height()*0.75)),
                'y': 0,
                'vx': random.uniform(-1, 1) * (1 + intensity_var.get()*0.25),
                'vy': random.uniform(1, 3) * (1 + intensity_var.get()*0.25),
                'size': random.uniform(2, 3 + intensity_var.get())
            })
    
        # Update snowflake positions (wind affects horizontal movement)
        for snowflake in snowflakes:
            # Default velocity scaled for 30 FPS and modified by intensity and wind
            snowflake['x'] += snowflake['vx'] * 0.5 + wind_var.get() * 0.2
            snowflake['y'] += snowflake['vy'] * 0.5
        
        redraw_canvas()
            
        # Calculate remaining time and schedule next frame
        elapsed_time = (time.time() - frame_start) * 1000  # Convert to ms
        delay = max(1, int(target_frame_time - elapsed_time))  # At least 1ms
        animation_id = canvas.after(delay, animate_snow)

    else:
        # Stop animation when snow is unchecked
        snowflakes = []
        if animation_id:
            canvas.after_cancel(animation_id)
            animation_id = None
        
        redraw_canvas()

# Toggle blizzard option visibility and state
def toggle_snow_options():
    if snow_var.get():
        intensity_slider.config(state=tk.NORMAL)
        wind_slider.config(state=tk.NORMAL)
        animate_snow()
    else:
        intensity_slider.config(state=tk.DISABLED)
        wind_slider.config(state=tk.DISABLED)

snow_check.config(command=toggle_snow_options)

# Randomize snowman button functionality
def randomize_snowman():
    bg_color_var.set(random.choice(["light blue", "white", "light gray", "green"]))
    snow_var.set(random.choice([True, False]))
    intensity_var.set(random.randint(0, 3))
    wind_var.set(random.uniform(-WIND_TOP_SPEED, WIND_TOP_SPEED))
    radius_var.set(random.randint(ZOOM_MIN, ZOOM_MAX))
    height_var.set(random.randint(0, HEIGHT_MAX))
    size_diff_var.set(random.uniform(SIZE_DIFF_MIN, SIZE_DIFF_MAX))
    hat_var.set(random.choice([True, False]))
    eyes_var.set(random.choice([True, False]))
    carrot_var.set(random.choice([True, False]))
    arms_var.set(random.choice([True, False]))
    buttons_var.set(random.choice([True, False]))
    scarf_var.set(random.choice([True, False]))
    fun_fact_label.config(text=random.choice(fun_facts))

    # Update
    update_intensity_label(intensity_var.get())
    update_wind_label(wind_var.get())
    update_height_label(height_var.get())
    update_size_diff_label(size_diff_var.get())
    redraw_canvas()
    toggle_snow_options()
randomize_button.config(command=lambda: randomize_snowman())

## Start the main event loop
animate_snow()
root.mainloop()