import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np

# Define process class
class Process:
    def __init__(self, pid, priority, arrival_time, burst_time):
        self.pid = pid
        self.priority = priority
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

# Define the CPU scheduler
class PriorityScheduler:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def schedule(self):
        # Sort the processes based on priority, then by arrival time
        self.processes.sort(key=lambda p: (p.priority, p.arrival_time))

        current_time = 0
        for process in self.processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            process.waiting_time = current_time - process.arrival_time
            process.response_time = process.waiting_time
            current_time += process.burst_time
            process.turnaround_time = process.waiting_time + process.burst_time

        # Calculate average times
        self.avg_waiting_time = sum(p.waiting_time for p in self.processes) / len(self.processes)
        self.avg_turnaround_time = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        self.avg_response_time = sum(p.response_time for p in self.processes) / len(self.processes)

    def plot_gantt_chart(self):
        # Create a Gantt chart
        fig, ax = plt.subplots()
        start_times = []
        durations = []
        labels = []

        current_time = 0
        for process in self.processes:
            if current_time < process.arrival_time:
                # Idle time
                start_times.append(current_time)
                durations.append(process.arrival_time - current_time)
                labels.append('')
                current_time = process.arrival_time

            start_times.append(current_time)
            durations.append(process.burst_time)
            labels.append(f'P{process.pid}')
            current_time += process.burst_time

        ax.barh(labels, durations, left=start_times, color='lightcoral')
        ax.set_xlabel('Time')
        ax.set_title('Gantt Chart')
        plt.show()

# Define the GUI
class ProcessEntryDialog(simpledialog.Dialog):
    def __init__(self, parent, pid):
        self.pid = pid
        self.priority = None
        self.arrival_time = None
        self.burst_time = None
        super().__init__(parent, title=f"Enter Process {pid} Data")

    def body(self, master):
        tk.Label(master, text=f"Process ID: P{self.pid}").grid(row=0, column=0, sticky='w')
        
        tk.Label(master, text="Priority:").grid(row=1, column=0, sticky='e')
        self.entry_priority = tk.Entry(master)
        self.entry_priority.grid(row=1, column=1)

        tk.Label(master, text="Arrival Time:").grid(row=2, column=0, sticky='e')
        self.entry_arrival_time = tk.Entry(master)
        self.entry_arrival_time.grid(row=2, column=1)

        tk.Label(master, text="Burst Time:").grid(row=3, column=0, sticky='e')
        self.entry_burst_time = tk.Entry(master)
        self.entry_burst_time.grid(row=3, column=1)

        return self.entry_priority

    def apply(self):
        try:
            self.priority = int(self.entry_priority.get())
            self.arrival_time = float(self.entry_arrival_time.get())
            self.burst_time = float(self.entry_burst_time.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid values for all fields.")
            self.priority = None
            self.arrival_time = None
            self.burst_time = None

class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ELZowzat & Bassel Scheduling Project")
        self.geometry("600x450")
        
        # Define color scheme
        self.background_color = "#f0f8ff"
        self.button_color = "#4682b4"
        self.text_color = "#000000"
        self.active_button_color = "#5f9ea0"
        self.icon_color = "#FFFFFF"  # Color for the icons
        
        # Custom font for a modern look
        self.custom_font = ("Helvetica", 12)
        
        self.configure(bg=self.background_color)

        self.processes = []

        # GUI widgets
        self.label_processes = tk.Label(
            self, text="Enter Number of Processes to Schedule:",
            bg=self.background_color, fg=self.text_color,
            font=self.custom_font
        )
        self.label_processes.pack(pady=10)

        self.entry_processes = tk.Entry(self, font=self.custom_font)
        self.entry_processes.pack(pady=5)

        # Button to add processes
        self.button_add_processes = tk.Button(
            self, text="Add Processes", bg=self.button_color, fg=self.icon_color,
            activebackground=self.active_button_color, font=self.custom_font,
            command=self.add_processes, width=20, height=2
        )
        self.button_add_processes.pack(pady=10)

        # Button to run the scheduler
        self.button_run = tk.Button(
            self, text="Run Scheduler", bg=self.button_color, fg=self.icon_color,
            activebackground=self.active_button_color, font=self.custom_font,
            command=self.run_scheduler, width=20, height=2
        )
        self.button_run.pack(pady=10)

        # Button to show Gantt chart
        self.button_show_gantt = tk.Button(
            self, text="Show Gantt Chart", bg=self.button_color, fg=self.icon_color,
            activebackground=self.active_button_color, font=self.custom_font,
            command=self.show_gantt_chart, width=20, height=2
        )
        self.button_show_gantt.pack(pady=10)

    def add_processes(self):
        try:
            num_processes = int(self.entry_processes.get())
            if num_processes <= 0:
                raise ValueError("Number of processes must be positive.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        
        self.processes = []
        
        for i in range(num_processes):
            pid = i + 1
            dialog = ProcessEntryDialog(self, pid)
            if dialog.priority is None or dialog.arrival_time is None or dialog.burst_time is None:
                return  # Invalid input; cancel adding processes
            process = Process(pid, dialog.priority, dialog.arrival_time, dialog.burst_time)
            self.processes.append(process)

        messagebox.showinfo("Processes Added", "Processes added successfully!")

    def run_scheduler(self):
        if not self.processes:
            messagebox.showerror("No Processes", "No processes to schedule.")
            return

        scheduler = PriorityScheduler()
        for process in self.processes:
            scheduler.add_process(process)

        scheduler.schedule()

        # Show results
        results = []
        for process in scheduler.processes:
            results.append(
                f"Process P{process.pid}:\n"
                f"Waiting Time: {process.waiting_time:.2f}\n"
                f"Turnaround Time: {process.turnaround_time:.2f}\n"
                f"Response Time: {process.response_time:.2f}\n"
            )

        results.append(
            f"Average Waiting Time: {scheduler.avg_waiting_time:.2f}\n"
            f"Average Turnaround Time: {scheduler.avg_turnaround_time:.2f}\n"
            f"Average Response Time: {scheduler.avg_response_time:.2f}\n"
        )

        messagebox.showinfo("Scheduling Results", "\n".join(results))

        self.scheduler = scheduler

    def show_gantt_chart(self):
        if hasattr(self, 'scheduler') and self.scheduler.processes:
            self.scheduler.plot_gantt_chart()
        else:
            messagebox.showerror("No Scheduler", "Run the scheduler first.")

# Run the GUI
if __name__ == "__main__":
    gui = SchedulerGUI()
    gui.mainloop()
