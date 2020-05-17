from hp_model import operation
import matplotlib.pyplot as plt


init = 0
state = 0
i = 0

cp1 = []
cp2 = []
erp = []
pu = []
efflist = []
last_state = 0
temperature = []
state_list = []
Q_list = []
while 1:
    if i >= 30:
        state = 0
    state_list.append(state)
    last_q = init
    Q, P_total, COP, P, eff, T, current_q = operation(state, last_q, 'Heater')
    cp1.append(P[0])
    cp2.append(P[1])
    erp.append(P[2])
    pu.append(P[3])
    efflist.append(eff)
    temperature.append(T)
    Q_list.append(current_q)
    i += 1
    init = Q
    last_state = state
    state = 100
    if i == 50:
        break

plt.figure()
plt.plot(cp1, label='cp1')
plt.plot(cp2, label='cp2')
plt.plot(erp, label='erp')
plt.plot(pu, label='pu')
plt.legend()
plt.xlabel('Minutes')
plt.ylabel('Power')
plt.show()

plt.figure()
plt.plot(efflist)
plt.xlabel('Minutes')
plt.ylabel('Efficiency')
plt.show()

plt.figure()
plt.plot(temperature)
plt.xlabel('Minutes')
plt.ylabel('Temperature')
plt.show()

plt.figure()
plt.plot(state_list)
plt.xlabel('Minutes')
plt.ylabel('State')
plt.show()

plt.figure()
plt.plot(Q_list)
plt.xlabel('Minutes')
plt.ylabel('Q')
plt.show()

print("Thermal input to the Room: %10.3f" % Q + "\n",
      "Total power consumption: %10.3f" % P_total + "\n",
      "Energy efficiency of heat pump: %10.3f" % COP)
