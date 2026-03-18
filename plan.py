'''
plan.py: 15-Day Transformation Plan for Realtime Process Dashboard
This file documents the step-by-step evolution from the old procedural code to the new class-based code,
with each day's changes explained in comments for reference and tracking purposes.
'''

'''
Day 1 -> Refactor into Class Structure
Change Explanation: The old procedural code is reorganized into a class-based structure for better modularity. The ProcessMonitor class encapsulates all dashboard functionality, improving maintainability and scalability.
Code Snippet:
class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Monitor Dashboard")
        self.root.geometry("1000x800")
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg='#1e1e1e')
        # Additional frame setup for header, info, graphs, and table
'''

'''
Day 2 -> Introduce Theme Configurations
Change Explanation: A themes dictionary is added to define dark and light mode styles. This centralizes color configurations, making it easier to manage and switch UI appearances dynamically.
Code Snippet:
themes = {
    "dark": {"bg": "#1a1a1a", "fg": "#ffffff", "accent": "#64b5f6"},
    "light": {"bg": "#f8f9fa", "fg": "#2d3436", "accent": "#1a237e"}
}

def setup_styles(self):
    style = ttk.Style()
    style.theme_use('clam')
    t = themes[self.current_theme]
    style.configure(".", background=t["bg"], foreground=t["fg"])
'''

'''
Day 3 -> Implement Theme Switching
Change Explanation: A theme toggle button and switching logic are added to the UI. This enhances user experience by allowing real-time switching between dark and light modes with a single click.
Code Snippet:
def setup_header(self):
    self.theme_btn = tk.Button(self.header_frame, text="🌙", command=self.toggle_theme)
    self.theme_btn.pack(side='right')

def toggle_theme(self):
    self.current_theme = "light" if self.current_theme == "dark" else "dark"
    self.setup_styles()
'''

'''
Day 4 -> Enhance Process Data Collection
Change Explanation: The process data collection is expanded to include username and creation time. This provides richer process details, enabling advanced filtering and display options in the dashboard.
Code Snippet:
def get_process_data(self):
    processes = {}
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'username', 'create_time']):
        processes[proc.info['pid']] = {
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'cpu': proc.info['cpu_percent'],
            'memory': proc.info['memory_info'].rss / 1024 / 1024,
            'username': proc.info['username'],
            'create_time': time.ctime(proc.info['create_time'])
        }
    return processes
'''

'''
Day 5 -> Add Memory Usage Graph
Change Explanation: A second graph is introduced to display memory usage trends alongside CPU usage. This gives users a fuller picture of system resource utilization in real time.
Code Snippet:
def setup_graphs(self):
    self.fig, (self.ax_cpu, self.ax_mem) = plt.subplots(1, 2, figsize=(12, 3))
    self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
    self.mem_history = deque(maxlen=50)
'''

'''
Day 6 -> Add Per-Core CPU Graphs
Change Explanation: Per-core CPU usage tracking and a graph mode toggle are implemented. This allows detailed monitoring of individual CPU cores, beneficial for multi-core system analysis.
Code Snippet:
def setup_graphs(self):
    self.cpu_history_per_core = [deque(maxlen=50) for _ in range(psutil.cpu_count())]
    self.graph_mode_var = tk.StringVar(value="overall")
    tk.Button(self.controls_frame, text="Per-Core", command=lambda: self.graph_mode_var.set("per-core")).pack()
'''

'''
Day 7 -> Add CPU Usage Filter
Change Explanation: A dropdown filter for CPU usage is added to the UI. This enables users to focus on processes exceeding a selected CPU usage threshold, improving process analysis efficiency.
Code Snippet:
def setup_filters(self):
    self.cpu_filter_var = tk.StringVar(value="All")
    ttk.OptionMenu(self.filter_frame, self.cpu_filter_var, "All", "All", "10", "25", command=self.apply_filters).pack()
'''

'''
Day 8 -> Add Memory Usage Filter
Change Explanation: A memory usage filter dropdown is introduced alongside the CPU filter. This helps users identify and focus on processes consuming significant memory, enhancing resource monitoring.
Code Snippet:
def setup_filters(self):
    self.mem_filter_var = tk.StringVar(value="All")
    ttk.OptionMenu(self.filter_frame, self.mem_filter_var, "All", "All", "50", "100", command=self.apply_filters).pack()
'''

'''
Day 9 -> Add User Type Filter
Change Explanation: A filter to display only system or user processes is added. This allows users to differentiate process ownership, aiding in system vs. user process monitoring.
Code Snippet:
def setup_filters(self):
    self.user_filter_var = tk.StringVar(value="All")
    ttk.OptionMenu(self.filter_frame, self.user_filter_var, "All", "All", "System", "User", command=self.apply_filters).pack()
'''

'''
Day 10 -> Implement Table Sorting
Change Explanation: Sorting functionality is added to the process table columns. This lets users sort processes by PID, name, CPU, etc., making it easier to analyze and prioritize process data.
Code Snippet:
def setup_process_table(self):
    for col in self.tree["columns"]:
        self.tree.heading(col, command=lambda c=col: self.sort_treeview(c, False))
'''

'''
Day 11 -> Add Start Process Button
Change Explanation: A button to launch new processes is added to the controls. This transforms the dashboard into an active management tool, allowing users to initiate applications directly.
Code Snippet:
def setup_controls(self):
    tk.Button(self.controls_frame, text="Start Process", command=self.start_new_process).pack()

def start_new_process(self):
    cmd = tk.simpledialog.askstring("Start Process", "Enter command:")
    if cmd:
        subprocess.Popen(cmd, shell=True)
'''

'''
Day 12 -> Add Export Data Button
Change Explanation: An export button is added to save process data as a CSV file. This enables users to archive or analyze process snapshots outside the dashboard, adding a practical feature.
Code Snippet:
def export_data(self):
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if filename:
        with open(filename, 'w') as f:
            f.write("PID,Name,CPU %,Memory (MB)\n")
            for proc in self.existing_processes.values():
                f.write(f"{proc['pid']},{proc['name']},{proc['cpu']},{proc['memory']}\n")
'''

'''
Day 13 -> Add Process Details on Double-Click
Change Explanation: Double-clicking a table row now shows detailed process info. This provides instant access to additional data like username and creation time, boosting interactivity.
Code Snippet:
def setup_process_table(self):
    self.tree.bind("<Double-1>", self.show_process_details)

def show_process_details(self, event):
    item = self.tree.identify_row(event.y)
    pid = int(self.tree.item(item)["values"][0])
    proc = self.existing_processes[pid]
    messagebox.showinfo("Details", f"PID: {pid}\nName: {proc['name']}")
'''

'''
Day 14 -> Add Status Bar
Change Explanation: A status bar is added to display real-time update info. This informs users about the last update time and process count, improving dashboard transparency.
Code Snippet:
def setup_status_bar(self):
    self.status_var = tk.StringVar()
    ttk.Label(self.status_frame, textvariable=self.status_var).pack()
'''

'''
Day 15 -> Final Refinements and Detailed Comments
Change Explanation: The code is polished, and detailed comments are added throughout. This ensures the final version is clean, consistent, and well-documented for future maintenance.
Code Snippet:
# Final code with detailed comments added throughout, e.g.,
# def update_dashboard(self):
#     # Updates the dashboard every second with fresh process data
#     self.existing_processes = self.get_process_data()
#     self.update_table()
#     self.update_graphs()
#     self.root.after(1000, self.update_dashboard)
'''