# -*- coding: utf-8 -*-
"""
@author: Zi'ang Liu, Junjie Jin & Tianhao Yu
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import random

from hp_model import operation
from room_model import roomTemp


 


def price(date,dataset):
    r"""
    :param date: choose the date of price --> int 
    :param dataset: daily price data  --> csv type
    :return: daily_price --> float
    """
    #1-366
    with open(dataset,'r') as csvfile:
        reader = csv.reader(csvfile)
        price = [row[3]for row in reader]
    price=price[1:]    
    price_list=[]
    for p in price:
        price_list.append(float(p))
    daily_price=[]
    for i in range((date-1)*48,date*48):
        p=price_list[i]
        daily_price.extend([p]*30)
    return daily_price

def temp(date,dataset):
    r"""
    :param date: choose the date of weather temperature --> int 
    :param dataset: daily weather temperature data  --> csv type
    :return: daily_price --> float
    """
    #1-366(1905)
    with open(dataset,'r') as csvfile2:
        reader2 = csv.reader(csvfile2)
        temp = [row[3]for row in reader2]
    temp=temp[1:]    
    temp_list=[]
    for t in temp:
        temp_list.append(float(t))
        if float(t)<0:
            print(t)
    daily_temp=[]
    for i in range((date-1)*24,date*24):
        t=temp_list[i]
        daily_temp.extend([t]*60)
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


def controloptimal(time, date, method_heatpump, demand, price_list, temp_list):
r"""
    :param time: total minute which need to analsying--> int should be delete 120
    :param date: choose the data to analysing --> int
    :param method_heatpump: type of String, should be 'heater' or 'cooler' to indicate the type of heat pump
    :param demand: user demand data --> list
    :param price_list: daily price data (name) --> 'name.csv' type
    :param temp: daily weather temperature data (name) --> 'name.csv' type
    :return: costlist --> list
             p_list --> list
             T_room --> list
             cost --> float
             newP --> float
    """
    control = []
    state = 0
    d_price = price(date,price_list)
    d_temp = temp(date,temp_list)

# initialize Room and Heat Pump Temperature model 
    Printer = False
    T_room = [d_temp[0]]
    Power = [0]
    heat_pumpT = [0]
    cost = 0
    Price = []
    newp = 0
    p_list = []
    costlist =[0]
    time = time
    for t in range(time):
        if demand[t] == 0:
            down = 1
        else:
            down = 0
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

        if (t + 30) < (len(d_price) - 1) and d_price[t + 30] >= 80 and d_t > demand[t]:
        # t+3, 30min can still be t. 3--no feeling
            if room_t > d_t + 3:
            # avoid 0 for control
                control.append(0)
            elif room_t < d_t + 1:
                control.append(10)
            else:
                control.append(round(round((d_t + 4 - room_t) * 50) / 10))

        elif demand[t + 120] <= demand[t]:
            if room_t > demand[t] - 2:
            # avoid 0 for control
                control.append(0)
            elif room_t < demand[t] - 4:
                control.append(10)
            else:
                control.append(round(round((demand[t] - 2 - room_t) * 50) / 10))

        elif (t + 30) < (len(d_price) - 1):
            if state == 0:
                control.append(0)
            elif state == 1:
                control.append(8)
            else:
            # print(len(d_price), t + 30, t)
                price_diff = d_price[t + 30] - d_price[t]
            # ave30-40 (4 is 10%)
                if price_diff > 4:
                    set_temp = demand[t] + 1.5
                elif price_diff < -4:
                    set_temp = demand[t] - 2.5
                else:
                    set_temp = demand[t] + price_diff / 2 - 0.5

                if room_t > set_temp + 1:
                # avoid 0 for control
                    control.append(0)
                elif room_t < set_temp - 1:
                    control.append(10)
                else:
                    control.append(round(round((set_temp + 1 - room_t) * 50) / 10))
    # connect Heat Pump
        if control[-1] != 0:
        # Q = 0
            Q, P_total, COP, P, eff, T, current_q = operation(control[-1], Power[-1], method_heatpump)
        # print(Q, P_total, COP, P, eff, T, current_q)
            P = P
        else:
            Q = 0
            T = 0
        #P = [0,0,0,0]


    # connect Room
        room_ct = roomTemp(T_room[-1], d_temp[t], Q * 1000, method_heatpump, Printer)
        heat_pumpT.append(T)
        T_room.append(room_ct)
        Power.append(Q)
        cost += Power[-1] * d_price[t] / 360000
        costlist.append(cost)
        newp += Power[-1]
        p_list.append(newp)
    return costlist,p_list,T_room,cost,newP



"""

for t in range(1440):
    room_t = T_room[-1]

    if room_t < demand[t] - 1:
        control.append(10)
    elif room_t > demand[t] + 1:
        control.append(0)
    else:
        control.append(5)
            
    if control[-1] != 0:
        # Q = 0
        Q, P_total, COP, P, eff, T, current_q = operation(control[-1], Power[-1], method_heatpump)
        # print(Q, P_total, COP, P, eff, T, current_q)
    else:
        Q = 0
        T = 0


    # connect Room
    room_ct = roomTemp(T_room[-1], d_temp[t], Q * 1000, method_heatpump, Printer)
    heat_pumpT.append(T)
    T_room.append(room_ct)
    Power.append(Q)
    cost += Power[-1] * d_price[t] / 360000
    costlist.append(cost)
    Price.append(cost)
    newp += Power[-1]
    p_list.append(newp)
    # print(Q, T, room_ct, control[-1])



for t in range(1440):
    room_t = T_room[-1]

    if room_t < demand[t] :
        control.append(10)

    else:
        control.append(0)
            
    if control[-1] != 0:
        # Q = 0
        Q, P_total, COP, P, eff, T, current_q = operation(control[-1], Power[-1], method_heatpump)
        # print(Q, P_total, COP, P, eff, T, current_q)
    else:
        Q = 0
        T = 0


    # connect Room
    room_ct = roomTemp(T_room[-1], d_temp[t], Q * 1000, method_heatpump, Printer)
    heat_pumpT.append(T)
    T_room.append(room_ct)
    Power.append(Q)
    cost += Power[-1] * d_price[t] / 360000
    costlist.append(cost)
    Price.append(cost)
    newp += Power[-1]
    p_list.append(newp)
    # print(Q, T, room_ct, control[-1])

"""