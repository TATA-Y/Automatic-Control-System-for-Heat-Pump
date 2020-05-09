from hp_model import operation

init = 0
last_q = init
state = 1
Q, steady, P_total, COP = operation(state, last_q, True, 'Cooler')

print(Q, steady, P_total, COP)