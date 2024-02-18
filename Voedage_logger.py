import csv
import matplotlib.pyplot as plt
import random
from datetime import datetime, timezone, timedelta
from itertools import count
from matplotlib.animation import FuncAnimation
import pytz

# Initialize lists to store voltage and amperage data
voltage_data = []
amperage_data = []
time_data = []

# Create a generator function to produce random voltage and amperage data
def generate_data():
    # Infinite loop to continuously generate data
    for i in count():
        # Generate random voltage and amperage data
        voltage = random.uniform(0, 10)
        amperage = random.uniform(0, 5)

        # Get current time in GMT
        current_time = datetime.now(pytz.timezone('Europe/Amsterdam'))

        # Append the data to the lists
        voltage_data.append(voltage)
        amperage_data.append(amperage)
        time_data.append(current_time)

        # Yield the data for real-time plotting
        yield current_time, voltage, amperage

# Function to update the plot and export data to CSV
def update_plot(frame):
    # Unpack the data
    time, voltage, amperage = frame

    # Calculate the current time
    current_time = datetime.now(timezone.utc)

    # Calculate the time window (last minute)
    time_window_start = max(current_time - timedelta(seconds=60), time_data[0])

    # Filter data within the last minute
    filtered_time_data = []
    filtered_voltage_data = []
    filtered_amperage_data = []
    for t, v, a in zip(time_data, voltage_data, amperage_data):
        if t >= time_window_start:
            filtered_time_data.append(t)
            filtered_voltage_data.append(v)
            filtered_amperage_data.append(a)

    # Convert filtered time data to relative time in seconds
    time_seconds = [(t - time_window_start).total_seconds() for t in filtered_time_data]

    # Clear previous plot
    plt.subplot(2, 1, 1).cla()
    plt.subplot(2, 1, 2).cla()

    # Plot voltage data
    plt.subplot(2, 1, 1)
    plt.plot(filtered_time_data, filtered_voltage_data, label='Voltage (V)', color='blue')
    plt.ylabel('Voltage (V)')
    plt.title('Real-time Voltage and Amperage Data')
    plt.grid(True)

    # Remove ticks and labels on the x-axis of the voltage subplot
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    # Plot amperage data
    plt.subplot(2, 1, 2)
    plt.plot(filtered_time_data, filtered_amperage_data, label='Amperage (A)', color='red')
    plt.xlabel('Time (GMT)')
    plt.ylabel('Amperage (A)')  # Adjust labelpad as needed
    plt.grid(True)
    # Adjust plot layout
    plt.tight_layout()

    # Export data to CSV
    export_to_csv(filtered_time_data, filtered_voltage_data, filtered_amperage_data)

# Function to export data to CSV
def export_to_csv(time_data, voltage_data, amperage_data):
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Voltage', 'Amperage'])
        for time, voltage, amperage in zip(time_data, voltage_data, amperage_data):
            writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), voltage, amperage])

# Create a figure and axis object
fig, ax = plt.subplots()

# Create a FuncAnimation object to update the plot in real-time
ani = FuncAnimation(fig, update_plot, frames=generate_data, interval=1000)

# Show the plot
plt.axis('off')
plt.show()
