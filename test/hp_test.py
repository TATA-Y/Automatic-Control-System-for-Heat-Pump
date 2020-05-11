from hp_model import operation

init = 0
last_q = init
state = 1
Q, P_total, COP = operation(state, last_q, True, 'Cooler')



print("Thermal input to the Room: %10.3f" % Q + "\n",
      "Total power consumption: %10.3f" % P_total + "\n",
      "Energy efficiency of heat pump: %10.3f" % COP)
