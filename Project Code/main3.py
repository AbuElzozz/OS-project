import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use('Agg')
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

        ax.barh(labels, durations, left=start_times, color='skyblue')
        ax.set_xlabel('Time')
        ax.set_title('Gantt Chart')
        plt.show()

# Define the GUI
class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ELZowzat Scheduling Project")
        self.geometry("400x300")

        self.processes = []

        # GUI widgets
        self.label_processes = tk.Label(self, text="# Number of Processes want to Enter:")
        self.label_processes.pack()

        self.entry_processes = tk.Entry(self)
        self.entry_processes.pack()

        self.button_add_processes = tk.Button(self, text="Add Processes", command=self.add_processes)
        self.button_add_processes.pack()

        self.button_run = tk.Button(self, text="Run Scheduler", command=self.run_scheduler)
        self.button_run.pack()

        self.button_show_gantt = tk.Button(self, text="Show Gantt Chart", command=self.show_gantt_chart)
        self.button_show_gantt.pack()

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

            try:
                priority = int(input(f"Enter priority for process {pid}: "))
                if priority < 0:
                    raise ValueError("Priority must be non-negative.")

                arrival_time = float(input(f"Enter arrival time for process {pid}: "))
                if arrival_time < 0:
                    raise ValueError("Arrival time must be non-negative.")

                burst_time = float(input(f"Enter burst time for process {pid}: "))
                if burst_time <= 0:
                    raise ValueError("Burst time must be positive.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
                return

            process = Process(pid, priority, arrival_time, burst_time)
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
