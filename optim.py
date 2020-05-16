# -*- coding: utf-8 -*-
"""
@author: Zi'ang Liu & Tianhao Yu
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import random

from hp_model import operation
from room_model import roomTemp

with open('tradingprice_201505_201604.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    price = [row[3] for row in reader]
price = price[1:]
price_list = []
for p in price:
    price_list.append(float(p))
#    if float(p)<0:
#        print(p)

with open('weather_data_sydney_airport_2015.csv', 'r') as csvfile2:
    reader2 = csv.reader(csvfile2)
    temp = [row[3] for row in reader2]
temp = temp[1:]
temp_list = []
for t in temp:
    temp_list.append(float(t))
    if float(t) < 0:
        print(t)


def price(date):
    # 1-366
    daily_price = []
    for i in range((date - 1) * 48, date * 48):
        p = price_list[i]
        daily_price.extend([p] * 30)
    return daily_price


def temp(date):
    # 1-366(1905)
    daily_temp = []
    for i in range((date - 1) * 24, date * 24):
        t = temp_list[i]
        daily_temp.extend([t] * 60)
    return daily_temp


def next_state(state, up, down, reach):
    if state == 0:
        if up:
            nstate = 1
        else:
            nstate = 0
    if state == 1:
        if reach:
            nstate = 2
        else:
            nstate = 1
        if down:
            nstate = 0
    if state == 2:
        if up:
            nstate = 1
        else:
            nstate = 2
        if down:
            nstate = 0

    return nstate


# example of demand
demand = []
demand.extend([0] * 7 * 60)
# 7am-8am 25c
demand.extend([25] * 1 * 60)
demand.extend([0] * 13 * 60)
# 9pm-12pm 26c
demand.extend([25] * 3 * 60)
# next day
demand.extend([0] * 2 * 60)

date = 100
d_price = price(date)
d_temp = temp(date)
control = []
state = 0

# initialize Room and Heat Pump Temperature model
method_heatpump = 'Heater'
Printer = False
T_room = [d_temp[0]]
Power = [0]

for t in range(1440):
    if demand[t] == 0:
        down = 1
    else:
        dowm = 0
    if demand[t - 1] < demand[t]:
        up = 1
    else:
        up = 0

    room_t = T_room[-1]
    ##?
    if room_t >= demand[t]:
        reach = 1
    else:
        reach = 0
    state = next_state(state, up, down, reach)
    d_t = max(demand[t + 30:t + 60])

    if (t + 30) < 1440 and d_price[t + 30] >= 100 and d_t > demand[t]:
        # t+3, 30min can still be t. 3--no feeling
        if room_t > d_t + 4:  ##?
            # avoid 0 for control
            control.append(0)
        elif room_t < d_t + 2:
            control.append(100)
        else:
            control.append(round((d_t + 4 - room_t) * 50))

    elif sum(demand[t + 30:t + 90]) == 0:
        if room_t > demand[t] - 1:  ##?
            # avoid 0 for control
            control.append(0)
        elif room_t < demand[t] - 3:
            control.append(100)
        else:
            control.append(round((demand[t] - 1 - room_t) * 50))

    else:
        if state == 0:
            control.append(0)
        elif state == 1:
            control.append(100)
        else:
            price_diff = d_price[t + 30] - d_price[t]
            # ave30-40 (4 is 10%)
            if price_diff > 4:
                set_temp = demand[t] + 2
            elif price_diff < -4:
                set_temp = demand[t] - 2
            else:
                set_temp = demand[t] + price_diff / 2

            if room_t > set_temp + 1:
                # avoid 0 for control
                control.append(0)
            elif room_t < set_temp - 1:
                control.append(100)
            else:
                control.append(round((set_temp + 1 - room_t) * 50))

    # connect Heat Pump
    if control[-1] != 0:
        Q, P_total, COP, P, eff, T, current_q = operation(control[-1], Power[-1], method_heatpump)
    else:
        Q = 0
    # print(control[-1], Power[-1])
    # print(Q, P_total, COP, P, eff, T, current_q)
    # connect Room
    room_ct = roomTemp(T_room[-1], d_temp[t], Q * 1000, method_heatpump, Printer)
    # print(T_room[-1], d_temp[t])
    # print(room_ct)
    T_room.append(room_ct)
    Power.append(Q)



plt.figure()
plt.plot(Power)
plt.ylabel('Power')
plt.xlabel('Minutes')
plt.title('Power Consumption Vs Time')
plt.legend()
plt.show()


plt.figure()
plt.plot(T_room, label='Room T')
plt.plot(d_temp, label='Environment T')
plt.plot(demand, label='Demand T')
plt.xlabel('Minutes')
plt.ylabel('Temperature')
plt.title('Temperature Vs Time')
plt.legend()
plt.show()

plt.figure()
plt.plot(control, label='control')
plt.plot(d_price, label='Price Forecast')
plt.xlabel('Minutes')
plt.title('Validation of Control system')
plt.legend()
plt.show()

