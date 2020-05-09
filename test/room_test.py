import time
import matplotlib.pyplot as plt
import numpy as np
from room_model import Room
import pandas as pd

# Room model test

start = time.time()
index = 1
current_t = -5
count = 1
ptime = [0]
ptemp = [current_t]
power = 4500
plt.figure('Draw')
room = Room(current_t, -5, power)
room.get_RoomInfo()
method_heatpump = 'Heater'
data = {'Time step': [index],
        'Heatpump type': [method_heatpump],
        'Heat input': [power],
        'Room temperature': [current_t],
        }
while 1:
    room = Room(current_t, -5, power)
    current_t = room.heatUp(False, method_heatpump)
    count += index
    ptime.append(count)
    ptemp.append(current_t)
    # time.sleep(index)
    data['Time step'].append(count)
    data['Heat input'].append(power)
    data['Room temperature'].append(current_t)
    data['Heatpump type'].append(method_heatpump)

    if count == 3600:
        power = 2 * power
        print(power)

    if count == 7200:
        power = 2 * power

    if abs(ptemp[-1] - ptemp[-2]) < 0.0001:
        current_t = room.heatUp(True, method_heatpump)
        break
ptime = np.array(ptime) / 60
plt.plot(ptime, ptemp)
plt.xlabel('Time in minute')
plt.ylabel('Temperature in ℃')
plt.title(method_heatpump + '@4500 W')
plt.show()

df = pd.DataFrame(data)
df.to_csv("Room.csv", sep=",")