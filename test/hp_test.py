from hp_model import operation

init = 0
last_q = init
state = 1
Q, steady, P_total, COP = operation(state, last_q, True, 'Cooler')

if steady == 1:
    steady = "Yes"
else:
    steady = "No"

print("Thermal input to the Room: %10.3f" % Q + "\n",
      "Does the heat pump enter a stable state: " + steady + "\n",
      "Total power consumption: %10.3f" % P_total + "\n",
      "Energy efficiency of heat pump: %10.3f" % COP)
