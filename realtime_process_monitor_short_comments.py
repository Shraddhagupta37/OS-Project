# Import the psutil module, which allows us to get information about running processes and system resource usage (like CPU and memory)
import psutil
# Import the tkinter module and give it the alias 'tk'. Tkinter is Python's standard library for creating graphical user interfaces (GUIs).
import tkinter as tk
# Import ttk from tkinter. ttk provides themed widgets (like modern-looking buttons and tables) for better UI appearance.
from tkinter import ttk
# Import the pyplot module from matplotlib and call it 'plt'. Matplotlib is a library for creating plots and graphs. 'pyplot' is its interface for drawing charts.
import matplotlib.pyplot as plt
# Import FigureCanvasTkAgg, which lets us embed matplotlib plots directly into a tkinter window (so our graphs appear inside the app).
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Import the threading module. This allows us to run certain tasks (like updating the UI) in the background without freezing the main window.
import threading
# Import the time module, which provides time-related functions like sleeping for a few seconds or getting the current time.
import time
# Import deque from collections. deque (double-ended queue) is a fast, memory-efficient way to store and update lists of items, like recent CPU usage data for plotting.
from collections import deque

# ----------------------
# Custom styling section
# ----------------------
# This function sets up the visual style (colors, fonts, etc.) for our tkinter widgets, making the UI look modern and consistent.
def setup_styles():  # Define a function to set up custom styles for the app
    # Create a Style object, which is used to configure the appearance of ttk widgets
    style = ttk.Style()
    # Set the base theme to 'clam'. 'clam' is a modern built-in theme in ttk that supports more customization than the default.
    style.theme_use('clam')  # Use 'clam' theme as base
    
    # Configure the appearance of the Treeview widget (used for tables/lists)
    # - background: Sets the color behind the rows
    # - foreground: Sets the text color
    # - fieldbackground: Sets the color behind entry fields (matches background for consistency)
    # - rowheight: Height of each row for better visibility
    style.configure("Treeview",
                   background="#2b2b2b",
                   foreground="white",
                   fieldbackground="#2b2b2b",
                   rowheight=25)
    
    # Configure the appearance of the Treeview headings (the column titles)
    # - background: Darker color for the header row
    # - foreground: White text for contrast
    # - relief: 'flat' gives a modern, flat look instead of a raised border
    style.configure("Treeview.Heading",
                   background="#1e1e1e",
                   foreground="white",
                   relief="flat")
    
    # Set how the Treeview rows look when selected
    # - background: Dark gray when a row is selected
    # - foreground: Text stays white when selected
    style.map("Treeview",
              background=[('selected', '#404040')],
              foreground=[('selected', 'white')])
    
    # Configure a custom style for buttons (Custom.TButton)
    # - background: Bright red color for emphasis (e.g., for important actions)
    # - foreground: White text for readability
    # - padding: Extra space inside the button for a larger clickable area
    # - font: Use Helvetica, size 10, bold for a modern and clear look
    style.configure("Custom.TButton",
                   background="#ff5252",
                   foreground="white",
                   padding=10,
                   font=('Helvetica', 10, 'bold'))

# Data collection
def get_process_data():
    processes = {}
    try:
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
            processes[proc.info['pid']] = {
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'state': proc.info['status'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_info'].rss / 1024 / 1024  # MB
            }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return processes

# GUI setup
root = tk.Tk()
root.title("Process Monitor Dashboard")
root.geometry("1000x800")
root.configure(bg='#1e1e1e')

# Setup custom styles
setup_styles()

# Create main frames
header_frame = ttk.Frame(root)
header_frame.pack(fill="x", padx=10, pady=5)

title_label = ttk.Label(header_frame, 
                       text="Process Monitor Dashboard",
                       font=('Helvetica', 16, 'bold'),
                       foreground="white",
                       background="#1e1e1e")
title_label.pack(side="left", pady=10)

# System info frame
info_frame = ttk.Frame(root)
info_frame.pack(fill="x", padx=10, pady=5)

cpu_label = ttk.Label(info_frame,
                     text="CPU Usage:",
                     font=('Helvetica', 10),
                     foreground="white",
                     background="#1e1e1e")
cpu_label.pack(side="left", padx=5)

memory_label = ttk.Label(info_frame,
                        text="Memory Usage:",
                        font=('Helvetica', 10),
                        foreground="white",
                        background="#1e1e1e")
memory_label.pack(side="left", padx=20)

# Graph frame
graph_frame = ttk.Frame(root)
graph_frame.pack(fill="both", expand=True, padx=10, pady=5)

# CPU graph with dark theme
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 3))
fig.patch.set_facecolor('#1e1e1e')
ax.set_facecolor('#2b2b2b')
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)
cpu_history = deque(maxlen=50)

# Table frame
table_frame = ttk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Scrollbar for treeview
scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

# Table for process info
tree = ttk.Treeview(table_frame,
                    columns=("PID", "Name", "State", "CPU %", "Memory (MB)"),
                    show="headings",
                    yscrollcommand=scrollbar.set)

scrollbar.config(command=tree.yview)

# Configure column widths and alignments
tree.heading("PID", text="PID")
tree.heading("Name", text="Name")
tree.heading("State", text="State")
tree.heading("CPU %", text="CPU %")
tree.heading("Memory (MB)", text="Memory (MB)")

tree.column("PID", width=80, anchor="center")
tree.column("Name", width=200, anchor="w")
tree.column("State", width=100, anchor="center")
tree.column("CPU %", width=100, anchor="center")
tree.column("Memory (MB)", width=120, anchor="center")

tree.pack(fill="both", expand=True)

# Control frame
control_frame = ttk.Frame(root)
control_frame.pack(fill="x", padx=10, pady=10)

# Kill process button with custom styling
kill_btn = ttk.Button(control_frame,
                      text="Kill Selected Process",
                      style="Custom.TButton")
kill_btn.pack(side="left", padx=5)

# Store existing processes
existing_processes = {}

def update_tree(processes):
    current_items = {tree.item(item)["values"][0]: item for item in tree.get_children()}
    
    for pid, proc in processes.items():
        values = (proc['pid'], proc['name'], proc['state'], f"{proc['cpu']:.1f}", f"{proc['memory']:.1f}")
        if pid in current_items:
            tree.item(current_items[pid], values=values)
            current_items.pop(pid)
        else:
            tree.insert("", "end", values=values)
    
    for item in current_items.values():
        tree.delete(item)

def update_system_info():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    cpu_label.config(text=f"CPU Usage: {cpu_percent:.1f}%")
    memory_label.config(text=f"Memory Usage: {memory.percent:.1f}%")

def update_graph():
    ax.clear()
    ax.plot(list(cpu_history), label="CPU Usage (%)", color='#00ff00', linewidth=2)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)  # Add grid lines to the plot for easier reading
    ax.set_facecolor('#2b2b2b')  # Set the background color of the plot area to dark gray
    canvas.draw()  # Redraw the canvas to show updated graphs

# -----------------------------
# Function: update_dashboard
# -----------------------------
# This function runs in a separate thread and keeps updating the dashboard in real time.
# It fetches the latest process data, updates the process table, system info, and graphs.
# Using 'root.after' schedules UI updates on the main thread (required for tkinter).
# The function sleeps for 2 seconds between updates to avoid overloading the CPU.
def update_dashboard():
    global existing_processes
    while True:
        try:
            processes = get_process_data()  # Get the latest list of running processes
            root.after(0, update_tree, processes)  # Schedule process table update on the main thread
            root.after(0, update_system_info)  # Schedule system info update
            cpu_history.append(psutil.cpu_percent())  # Add current CPU usage to history for graph
            root.after(0, update_graph)  # Schedule graph update
            existing_processes = processes  # Store the latest process list
            time.sleep(2)  # Wait 2 seconds before next update
        except Exception as e:
            print(f"Error in update: {e}")  # Print any errors that occur
            time.sleep(1)  # Wait a bit before retrying if there's an error

# -----------------------------
# Function: kill_process
# -----------------------------
# This function is called when the user clicks the 'Kill' button.
# It finds the selected process in the table, gets its PID (Process ID),
# and then tries to terminate (kill) that process using psutil.
def kill_process():
    selected = tree.selection()  # Get the selected row(s) in the process table
    if selected:
        pid = int(tree.item(selected[0])["values"][0])  # Get the PID from the first column of the selected row
        try:
            proc = psutil.Process(pid)  # Create a Process object for the given PID
            proc.terminate()  # Attempt to terminate (kill) the process
        except psutil.NoSuchProcess:
            print(f"Process {pid} not found.")  # Handle the case where the process no longer exists

# Link the 'Kill' button to the kill_process function so that clicking the button will call the function above
kill_btn.config(command=kill_process)

# -------------------------------------
# Start the background update thread
# -------------------------------------
# We use threading so that the dashboard keeps updating in the background
# without freezing the main tkinter window. The 'daemon=True' flag means
# the thread will automatically close when the main program exits.
thread = threading.Thread(target=update_dashboard, daemon=True)
thread.start()  # Start the background thread

root.mainloop()








