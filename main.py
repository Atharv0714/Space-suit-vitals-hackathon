# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.widgets import Button as MplButton
from datetime import datetime

# Initialize the main GUI window
window = tk.Tk()
window.title("Enhanced Suit and Health Tracker with Device Integration")
window.configure(
    bg='#f0f0f0')  # Set a light grey background color for the window

# Configure the style for buttons and labels using ttk.Style
style = ttk.Style()
style.configure('TButton', font=('Times New Roman', 10), background='#f0f0f0')
style.configure('TLabel', font=('Times New Roman', 10), background='#f0f0f0')

# Dictionary to store health metrics data
health_metrics = {
    'heart_rate': [],
    'oxygen_level': [],
    'BMI': [],
    'hydration': [],
}

# Define healthy ranges for each metric
healthy_ranges = {
    'heart_rate': (60, 100),  # beats per minute
    'oxygen_level': (95, 100),  # percent saturation
    'BMI': (18.5, 24.9),  # Body Mass Index range
    'hydration': (45, 75),  # percent, conceptual representation
}


# Function to update health metrics
def update_health_metric(metric, value):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    health_metrics[metric].append((now, float(value)))
    check_health_range(metric, float(
        value))  # Call function to check if value is within the healthy range


# Function to check if the metric value is within the healthy range
def check_health_range(metric, value):
    min_val, max_val = healthy_ranges[metric]
    if not min_val <= value <= max_val:
        warning_msg = f"Your {metric.replace('_', ' ')} of {value} is outside the healthy range ({min_val} to {max_val})."
        # Determine the condition message based on the metric and its value
        condition_message = ""
        if metric == "heart_rate":
            condition_message = "Low heart rate (bradycardia)" if value < min_val else "High heart rate (tachycardia)"
        elif metric == "oxygen_level" and value < min_val:
            condition_message = "Low blood oxygen levels (hypoxemia)"
        elif metric == "BMI":
            condition_message = "Underweight" if value < min_val else "Overweight or obesity"
        elif metric == "hydration":
            condition_message = "Dehydration" if value < min_val else "Overhydration"
        full_message = f"{warning_msg}\nPossible condition: {condition_message}.\nPlease consult a healthcare professional."
        messagebox.showwarning("Health Alert", full_message)


# Function to visualize a specific health metric over time
def visualize_metric(metric):
    if not health_metrics[metric]:
        messagebox.showinfo("Info", "No data to visualize.")
        return
    times, values = zip(*health_metrics[metric])  # Unpack times and values
    times = [datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
             for time in times]  # Convert string times to datetime objects

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, values, marker='o',
            label=metric.title())  # Plot the metric values over time

    # Format the date on the x-axis for better readability
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()

    # Highlight the healthy range on the graph
    min_val, max_val = healthy_ranges[metric]
    ax.axhline(y=min_val, color='r', linestyle='--', label='Min healthy value')
    ax.axhline(y=max_val, color='g', linestyle='--', label='Max healthy value')
    ax.fill_between(times, min_val, max_val, color='yellow', alpha=0.1)

    ax.set_title(f"{metric.replace('_', ' ').title()} Over Time")
    ax.set_xlabel('Time')
    ax.set_ylabel(metric.title())
    plt.legend()

    # Add a "Close Plot" button to the graph for better navigation
    close_button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
    close_button = MplButton(close_button_ax,
                             'Close Plot',
                             color='lightblue',
                             hovercolor='lightskyblue')
    close_button.on_clicked(lambda event: plt.close(
        fig))  # Close the plot window when the button is clicked

    plt.show()


# Function to visualize all metrics on a cumulative graph
def visualize_all_metrics():
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['blue', 'green', 'red',
              'purple']  # Color coding for different metrics
    for idx, (metric, data) in enumerate(health_metrics.items()):
        if data:
            times, values = zip(*data)
            times = [
                datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in times
            ]
            ax.plot(times,
                    values,
                    linestyle='-',
                    marker='o',
                    color=colors[idx],
                    label=metric.title())  # Plot each metric

    ax.xaxis.set_major_formatter(
        DateFormatter('%Y-%m-%d %H:%M'))  # Format date on x-axis
    fig.autofmt_xdate()

    ax.set_title("Cumulative Health Metrics Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Metrics Values")
    plt.legend()

    # Add a "Close Plot" button to the graph
    close_button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
    close_button = MplButton(close_button_ax,
                             'Close Plot',
                             color='lightblue',
                             hovercolor='lightskyblue')
    close_button.on_clicked(lambda event: plt.close(fig))

    plt.show()


# Function to generate and display a transcript of the latest health metrics
def generate_and_send_transcript():
    transcript = "Health and Suit Metrics Transcript\n"
    transcript += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    for metric, values in health_metrics.items():
        latest_value = values[-1][
            1] if values else "N/A"  # Get the latest value or indicate as N/A
        transcript += f"{metric.replace('_', ' ').title()}: {latest_value}\n"
    messagebox.showinfo("Transcript Ready to Send", transcript)


# Set up the user interface for inputting health stats
for i, metric in enumerate(health_metrics.keys()):
    label = ttk.Label(window,
                      text=f"{metric.replace('_', ' ').title()}:",
                      style='TLabel')
    label.grid(column=0, row=i, sticky=tk.W, padx=10, pady=5)
    entry = ttk.Entry(window, font=('Times New Roman', 10))
    entry.grid(column=1, row=i, padx=10, pady=5)
    update_button = ttk.Button(
        window,
        text=f"Update {metric.replace('_', ' ').title()}",
        command=lambda m=metric, e=entry: update_health_metric(m, e.get()),
        style='TButton')
    update_button.grid(column=2, row=i, padx=10, pady=5, sticky='ew')
    visualize_button = ttk.Button(
        window,
        text=f"Visualize {metric.replace('_', ' ').title()}",
        command=lambda m=metric: visualize_metric(m),
        style='TButton')
    visualize_button.grid(column=3, row=i, padx=10, pady=5, sticky='ew')

# Ensure buttons have equal width
window.grid_columnconfigure(2, uniform="group1")
window.grid_columnconfigure(3, uniform="group1")

# Button to generate and send the health transcript
send_transcript_button = ttk.Button(window,
                                    text="Generate and Send Transcript",
                                    command=generate_and_send_transcript,
                                    style='TButton')
send_transcript_button.grid(column=0,
                            row=len(health_metrics),
                            columnspan=4,
                            padx=10,
                            pady=5,
                            sticky='ew')

# Button to visualize all metrics on a cumulative graph
visualize_all_button = ttk.Button(window,
                                  text="Visualize All Metrics",
                                  command=visualize_all_metrics,
                                  style='TButton')
visualize_all_button.grid(column=0,
                          row=len(health_metrics) + 1,
                          columnspan=4,
                          padx=10,
                          pady=10,
                          sticky='ew')

window.mainloop()
