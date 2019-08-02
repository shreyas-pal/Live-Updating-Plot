import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import
import numbers
from building_data_requests import get_value


# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')


def live_plotter(x_vec, y1_data, line1, identifier='', pause_time=15):
    if line1 == []:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        # update plot label/title
        plt.ylabel('kWH')
        plt.title('Andove High (Main kW) Power'.format(identifier))
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1


# the function below is for updating both x and y values (great for updating dates on the x-axis)
def live_plotter_xy(x_vec, y1_data, line1, identifier='', pause_time=0.01):
    if line1 == []:
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        line1, = ax.plot(x_vec, y1_data, 'r-o', alpha=0.8)
        plt.ylabel('Power (kW)')
        plt.title("AHS Main")
        plt.xlabel('Elapsed Time (Seconds)')
        plt.show()

    line1.set_data(x_vec, y1_data)
    plt.xlim(np.min(x_vec), np.max(x_vec))
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])

    plt.pause(pause_time)

    return line1

df = pd.read_csv(r"C:\Users\shrey\OneDrive\Documents\5 Programming\Energize\Learning Pandas\buildingEnergyApi-master\csv\ahs_power.csv")
main_row = df[df['Label'] == 'Main (kW)']

def get_reading():
    value, units = get_value(main_row['Facility'], main_row['Meter'], live=True)
    value = float(value) if isinstance(value, numbers.Number) else ''
    units = units if units else ''
    return value

max_points = 20
update_interval = 5

x_vec = np.ndarray(shape=(1,))
y_vec = np.ndarray(shape=(1,))
y_vec = np.append(y_vec[1:], get_reading())
line1 = []
while True:
    line1 = live_plotter_xy(x_vec, y_vec, line1, pause_time=update_interval)
    reading = get_reading()
    if x_vec.size < max_points:
        x_vec = np.append(x_vec, [x_vec[-1] + update_interval])
    else:
        x_vec = np.append(x_vec[1:], [x_vec[-1] + update_interval])

    if y_vec.size < max_points:
        y_vec = np.append(y_vec, [reading])
    else:
        y_vec = np.append(y_vec[1:], [reading])
