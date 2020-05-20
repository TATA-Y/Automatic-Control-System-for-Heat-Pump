# Automatic-Control-System-for-Heat-Pump

This Automatic Control System is to provide simulation kits for heat pumps and room models. With this software package, you can determine the relative reasonable working power of the heat pump according to the weather, price data, and user demand. It can automatically adjust the heat pump status in real-time according to electricity cost and user demands. The control system will choose a state (percentage of heat pump working power) base on price change, weather temperature change, and solar change to reduce the electricity fee. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

If you have a working Python3 environment, use pypi to install the latest tespy version:

```
pip install tespy
```

Also, you may need to install the following package using pypi

```
pip install prettytable
```

### Installing

If you have a Git environment, use git to install the latest version:

```
git clone https://github.com/Tianhao-Y/Automatic-Control-System-for-Heat-Pump.git
```

End with an example of getting some data out of the system or using it for a little demo
### Usage
```
from optim import controloptimal

Costlist, p_list, T_room, cost, newP = controloptimal(time, date, Method, demand, Price_file, weather_file)
```
Note: the detail could be found from [User Guide Document](https://github.com/Tianhao-Y/Automatic-Control-System-for-Heat-Pump/blob/master/User-Guide.pdf)
## Running the tests

### Break down into subsystem tests

Test the room model and heat pump model can functional well. Run in terminal

```
cd test
python room_test.py
python hp_test.
```

## Built With

* [TESPy](https://github.com/oemof/tespy) - The Heat Pump Simulation used

## Authors

* **Tianhao Yu** 
* **Mengzhou Wang** 
* **Bin Dong** 
* **Yunjie Jin** 
* **Zi'ang Liu** 
* **Weicong Zhang**

See also the list of [contributors](https://github.com/Tianhao-Y/Automatic-Control-System-for-Heat-Pump/graphs/contributors) who participated in this project.

## Some issues to know

1. The test environment is
    - Python 3.7.0
    - TESpy 0.2.2

2. If you want to speed up the running speed of the program, you need to delete the print items and error items in TESpy.


## License
Copyright (c) 2020 (Australian National University Heat Pump group)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments

Key parts of this project require the following scientific software packages: Matplotlib[@Matplotlib], NumPy [@NumPy], Pandas [@Pandas]. Other packages implemented are prettytable, TESpy, and Math.


