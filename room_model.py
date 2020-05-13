import time
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd


class Room(object):
    wall = 1.048
    window = 1.1
    wallArea = [70, 10]
    airExchange = 1
    ventilation = 0.33
    area = 100
    height = 3

    def __init__(self, room_temperature, environment_temperature, power):
        r"""
            :param density_a: air density in kg/m^3
            :param capacity_a: the heat capacity of the air J/（kg·℃）
            :param envirtemp: environment temperature in Degrees Celsius
            :param roomtemp: room temperature in Degrees Celsius
            :param power: input heat pump power W
            :return: current temperature in the room  C
        """
        #        self.setpup_temperature = setpup_temperature
        self.roomtemp = room_temperature
        self.envirtemp = environment_temperature
        self.density_a = 1.29
        self.capacity_a = 10050
        self.power = power

    def set_RoomInfo(self, wall, window, wallArea, airExchange, ventilation, area, height):
        r"""
            :param area: the size of the room in m^2
            :param height: the height of the room in m
            :param airExchange: air exchange rate m^3/s
            :param wall: The heat loss of the walls W/m^2*℃
            :param window: The heat loss of the windows W/m^2*℃
            :param ventilation: coefficient of ventilation W/m^3*℃
            :param wallArea: the area of walls and windows should be a list --> [area_walls, area_windows] m^2
        """
        Room.wall = wall
        Room.window = window
        Room.wallArea = wallArea
        Room.airExchange = airExchange
        Room.ventilation = ventilation
        Room.area = area
        Room.height = height

    def get_RoomInfo(self):
        """Print information of the Room's properties"""

        table = PrettyTable(["Property of the Room", "Value"])
        table.add_row(['The heat loss of the walls in W/m^2*℃', Room.wall])
        table.add_row(['The heat loss of the windows in W/m^2*℃', Room.window])
        table.add_row(['The area of walls and windows in m^2', Room.wallArea])
        table.add_row(['The air exchange rate in m^3/s', Room.airExchange])
        table.add_row(['The coefficient of ventilation in W/m^3*℃', Room.ventilation])
        table.add_row(['The area of room in m^2', Room.area])
        table.add_row(['The height of room in m', Room.height])

        print(table)

    def naturalCooling(self):
        # from the walls and windows
        qWall = Room.wall * Room.wallArea[0] * abs(self.roomtemp - self.envirtemp)
        qWindow = Room.window * Room.wallArea[1] * abs(self.roomtemp - self.envirtemp)

        # from the air flow
        qAir = Room.area * Room.height * Room.airExchange * Room.ventilation * abs(self.roomtemp - self.envirtemp)

        qLoss = qWall + qWindow + qAir
        return qLoss  # unit W

    def heatUp(self, printer, method):

        r"""
        :param time: how long it takes
        :param method: type of String, should be 'heater' or 'cooler' to indicate the type of heat pump
        :param printer: Boolean whether to print out the result
        :return: update_t, what the temperature will be after 1 sec
        """

        if method == 'Heater':
            k = -1
        elif method == 'Cooler':
            k = 1

        qLoss = self.naturalCooling() * k
        power = -k * self.power + qLoss
        # self.roomtemp = self.roomtemp  # +273.15
        mass_air = self.density_a * Room.area
        diff_t = power / mass_air / self.capacity_a

        update_t = self.roomtemp + diff_t  # -273.15

        # print out the result
        if printer:
            table = PrettyTable(["Output", "Value"])
            table.add_row(['An estimate of heat loss in house in W', round(qLoss, 2)])
            table.add_row(['The temperature after 1 seconds in ℃', round(update_t, 2)])

            print(table)

        return update_t


def roomTemp(room_temp, environment_temperature, power, method_heatpump, Printer):
    r"""
    :param Printer: Print information or not --> boolean
    :param room_temp: room temperature in Degrees Celsius --> float
    :param environment_temperature: environment temperature in Degrees Celsius --> float
    :param power: input heat pump power W --> float
    :param method_heatpump: whether it is heater or not --> string "Heater" or "Cooler"
    :return: the Update Temperature
    """
    
    room = Room(room_temp, environment_temperature, power)
    
    temp = room.heatUp(False, method_heatpump)
    
    if Printer:
        room.get_RoomInfo()
        
    return temp


# example usage

if __name__ == '__main__':

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
