import matplotlib
matplotlib.use('gtk4agg')
import gi
gi.require_version('Gtk', '4.0')
import matplotlib.pyplot as plt
import numpy as np
from gi.repository import Gtk, GLib, GObject

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
class SchedulerGUI(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.priorityscheduler")

        # Processes list
        self.processes = []

        # Set up the application window
        self.connect("activate", self.on_activate)
        
    def on_activate(self, app):
        # Create the main window
        self.window = Gtk.ApplicationWindow(application=app)
        self.window.set_title("Priority Scheduler")
        self.window.set_default_size(400, 300)
        
        # Create the vertical box to hold widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.window.set_child(vbox)

        # Create entry widgets for input
        self.entry_processes = Gtk.Entry()
        self.entry_processes.set_placeholder_text("Number of Processes")
        vbox.append(self.entry_processes)
        
        # Add processes button
        button_add_processes = Gtk.Button(label="Add Processes")
        button_add_processes.connect("clicked", self.on_add_processes)
        vbox.append(button_add_processes)

        # Run scheduler button
        button_run = Gtk.Button(label="Run Scheduler")
        button_run.connect("clicked", self.on_run_scheduler)
        vbox.append(button_run)

        # Show Gantt Chart button
        button_show_gantt = Gtk.Button(label="Show Gantt Chart")
        button_show_gantt.connect("clicked", self.on_show_gantt_chart)
        vbox.append(button_show_gantt)

        # Show results in a text view
        self.textview_results = Gtk.TextView()
        vbox.append(self.textview_results)




    def on_add_processes(self, button):
        try:
            num_processes = int(self.entry_processes.get_text())
            if num_processes <= 0:
                raise ValueError("Number of processes must be positive.")
        except ValueError as e:
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text=str(e),
            )
            dialog.run()
            dialog.destroy()
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
                dialog = Gtk.MessageDialog(
                    transient_for=self.window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CLOSE,
                    text=str(e),
                )
                dialog.run()
                dialog.destroy()
                return

            process = Process(pid, priority, arrival_time, burst_time)
            self.processes.append(process)

        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Processes added successfully!",
        )
        dialog.run()
        dialog.destroy()

    def on_run_scheduler(self, button):
        if not self.processes:
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text="No processes to schedule.",
            )
            dialog.run()
            dialog.destroy()
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

        # Display results in the text view
        text_buffer = self.textview_results.get_buffer()
        text_buffer.set_text("\n".join(results))

        self.scheduler = scheduler

    def on_show_gantt_chart(self, button):
        if hasattr(self, 'scheduler') and self.scheduler.processes:
            self.scheduler.plot_gantt_chart()
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSED,
                text="Run the scheduler first.",
            )
            dialog.run()
            dialog.destroy()

# Run the GUI
if __name__ == "__main__":
    app = SchedulerGUI()
    app.run()
