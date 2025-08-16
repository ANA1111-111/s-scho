import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")

# Style configuration
style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
style.configure("Header.TLabel", background="#e0f7e0", font=("Helvetica", 16, "bold"))
style.configure("TButton", background="#f0f0f0", font=("Helvetica", 10))

# Create the main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Header
header = ttk.Label(main_frame, text="School Management System", style="Header.TLabel")
header.grid(row=0, column=0, columnspan=4, pady=(0, 20))

# Sections
sections = [
    ("Students", 6), ("Fee Collection", 3), ("Banks", 3),
    ("Teachers", 2), ("Subjects", 2), ("Classes", 3),
    ("Streams", 2), ("Hostels", 1), ("Timetables", 0),
    ("Events", 1), ("Notices", 1), ("Exam Results", 1)
]

# Create section frames
for i, (section, count) in enumerate(sections):
    frame = ttk.Frame(main_frame, padding="10", borderwidth=1, relief="solid")
    frame.grid(row=i//4 + 1, column=i%4, padx=10, pady=10, sticky="nsew")
    
    label = ttk.Label(frame, text=section)
    label.pack(pady=(0, 5))
    
    count_label = ttk.Label(frame, text=str(count))
    count_label.pack(pady=(0, 5))
    
    view_button = ttk.Button(frame, text="View")
    view_button.pack()

# Start the application
root.mainloop()
