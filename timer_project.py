import tkinter as tk
from tkinter import font
from tkinter import ttk
from datetime import datetime

class timeapp:
    def __init__(self, master):
        self.master = master
        master.title("⏱ Timer App")
        master.geometry("750x550")
        master.resizable(False, False)
        master.configure(bg="#1e1e2e")
        
        # Define custom fonts
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        label_font = font.Font(family="Helvetica", size=14)
        display_font = font.Font(family="Courier", size=48, weight="bold")
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Title
        title_label = tk.Label(master, text="⏱ TIMER APP", font=title_font, 
                               bg="#1e1e2e", fg="#00d4ff")
        title_label.pack(pady=(20, 10))
        
        # Local time display
        self.clock_label = tk.Label(master, text="", font=font.Font(family="Helvetica", size=12),
                                    bg="#1e1e2e", fg="#ff9500")
        self.clock_label.pack(pady=2)
        self.update_clock()
        
        # Input frame
        input_frame = tk.Frame(master, bg="#1e1e2e")
        input_frame.pack(pady=10)
        
        self.label = tk.Label(input_frame, text="Enter time in seconds:", 
                             font=label_font, bg="#1e1e2e", fg="#ffffff")
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(input_frame, font=label_font, width=12,
                             bg="#313244", fg="#00d4ff", 
                             insertbackground="#00d4ff", 
                             bd=2, relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, padx=5)

        # Display label for countdown
        self.time_label = tk.Label(master, text="00:00", font=display_font,
                                   bg="#1e1e2e", fg="#00ff88")
        self.time_label.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(master, text="Ready to start", 
                                    font=label_font, bg="#1e1e2e", fg="#a0a0a0")
        self.status_label.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(master, bg="#1e1e2e")
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="▶ Start Timer", 
                                     command=self.start_timer,
                                     font=button_font,
                                     bg="#00d4ff", fg="#1e1e2e",
                                     activebackground="#00ffff",
                                     activeforeground="#1e1e2e",
                                     padx=30, pady=12, 
                                     bd=0, relief=tk.FLAT,
                                     cursor="hand2")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(button_frame, text="⟲ Reset",
                                      command=self.reset_timer,
                                      font=button_font,
                                      bg="#ff6b6b", fg="#6B6B6B",
                                      activebackground="#ff8888",
                                      activeforeground="#ffffff",
                                      padx=30, pady=12,
                                      bd=0, relief=tk.FLAT,
                                      cursor="hand2")
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        self.time_remaining = 0
        self.is_running = False
        self.total_time = 0  # Store original time for progress calculation

        pause_button = tk.Button(button_frame, text="⏸ Pause",
                                    command=self.pause_timer,
                                    font=button_font,
                                    bg="#ff0000", fg="#ffffff",
                                    activebackground="#ff4444",
                                    activeforeground="#ffffff",
                                    padx=30, pady=12,
                                    bd=0, relief=tk.FLAT,
                                    cursor="hand2")
        pause_button.pack(side=tk.LEFT, padx=10)

        self.resume_button = tk.Button(button_frame, text="▶ Resume",
                                    command=self.resume_timer,
                                    font=button_font,
                                    bg="#00ff00", fg="#1e1e2e",
                                    activebackground="#88ff88",
                                    activeforeground="#1e1e2e",
                                    padx=30, pady=12,
                                    bd=0, relief=tk.FLAT,
                                    cursor="hand2")
        self.resume_button.pack(side=tk.LEFT, padx=10)

        # Progress bar frame
        progress_frame = tk.Frame(master, bg="#1e1e2e")
        progress_frame.pack(pady=15, padx=20, fill=tk.X)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', 
                                            length=400, value=0,
                                            style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, expand=True)


    def start_timer(self):
        try:
            time_in_seconds = int(self.entry.get())
            if time_in_seconds <= 0:
                self.status_label.config(text="❌ Please enter a positive number", fg="#ff6b6b")
                return
            self.total_time = time_in_seconds  # Store total time
            self.time_remaining = time_in_seconds
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)
            self.status_label.config(text="⏳ Timer running...", fg="#00ff88")
            self.update_timer(time_in_seconds)
        except ValueError:
            self.status_label.config(text="❌ Please enter a valid number", fg="#ff6b6b")

    def update_timer(self, time_left):
        if time_left >= 0 and self.is_running:
            self.time_remaining = time_left  # Store current time for pause/resume
            minutes = time_left // 60
            seconds = time_left % 60
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            
            # Update progress bar
            if self.total_time > 0:
                progress = ((self.total_time - time_left) / self.total_time) * 100
                self.progress_bar['value'] = progress
            
            self.master.after(1000, lambda: self.update_timer(time_left - 1))
        elif self.is_running:
            self.time_label.config(text="00:00")
            self.progress_bar['value'] = 100  # Full when complete
            self.status_label.config(text="✓ Time's up!", fg="#00ff88")
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.entry.config(state=tk.NORMAL)
    
    def reset_timer(self):
        self.is_running = False
        self.time_remaining = 0
        self.total_time = 0
        self.time_label.config(text="00:00")
        self.progress_bar['value'] = 0  # Reset progress bar
        self.status_label.config(text="Ready to start", fg="#a0a0a0")
        self.start_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)

    def pause_timer(self):
        self.is_running = False
        self.status_label.config(text="⏸ Timer paused", fg="#ff6b6b")
        self.start_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)

    def resume_timer(self):
        if self.time_remaining > 0:
            self.is_running = True
            self.status_label.config(text="⏳ Timer running...", fg="#00ff88")
            self.update_timer(self.time_remaining)

    def update_clock(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.clock_label.config(text=f"🕐 Current Time: {current_time}")
        self.master.after(1000, self.update_clock)

    def select_local_time(self):
        value = self.timezone_var.get()
        if value == "local":
            self.update_clock()
        else:
            self.clock_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = timeapp(root)
    root.mainloop()