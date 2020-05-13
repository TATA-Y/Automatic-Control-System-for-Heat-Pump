from tespy.networks import network
from tespy.components import (sink, source, splitter, compressor, condenser,
                              pump, heat_exchanger_simple, valve, drum,
                              heat_exchanger, cycle_closer)
from tespy.connections import connection, ref
from tespy.tools.characteristics import char_line
from tespy.tools.characteristics import load_default_char as ldc

import math


class HeatPump(object):
    # define the structure of heat pump

    # %% network

    nw = network(fluids=['water', 'NH3', 'air'],
                 T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

    # %% components

    # sources & sinks

    cc = cycle_closer('coolant cycle closer')
    cb = source('consumer back flow')
    cf = sink('consumer feed flow')
    amb = source('ambient air')
    amb_out1 = sink('sink ambient 1')
    amb_out2 = sink('sink ambient 2')

    # ambient air system

    sp = splitter('splitter')
    pu = pump('pump')

    # consumer system

    cd = condenser('condenser')
    dhp = pump('district heating pump')
    cons = heat_exchanger_simple('consumer')

    # evaporator system

    ves = valve('valve')
    dr = drum('drum')
    ev = heat_exchanger('evaporator')
    su = heat_exchanger('superheater')
    erp = pump('evaporator reciculation pump')

    # compressor-system

    cp1 = compressor('compressor 1')
    cp2 = compressor('compressor 2')
    ic = heat_exchanger('intercooler')

    # %% connections

    # consumer system

    c_in_cd = connection(cc, 'out1', cd, 'in1')
    cb_dhp = connection(cb, 'out1', dhp, 'in1')
    dhp_cd = connection(dhp, 'out1', cd, 'in2')
    cd_cons = connection(cd, 'out2', cons, 'in1')
    cons_cf = connection(cons, 'out1', cf, 'in1')
    nw.add_conns(c_in_cd, cb_dhp, dhp_cd, cd_cons, cons_cf)

    # connection condenser - evaporator system

    cd_ves = connection(cd, 'out1', ves, 'in1')
    nw.add_conns(cd_ves)

    # evaporator system

    ves_dr = connection(ves, 'out1', dr, 'in1')
    dr_erp = connection(dr, 'out1', erp, 'in1')
    erp_ev = connection(erp, 'out1', ev, 'in2')
    ev_dr = connection(ev, 'out2', dr, 'in2')
    dr_su = connection(dr, 'out2', su, 'in2')
    nw.add_conns(ves_dr, dr_erp, erp_ev, ev_dr, dr_su)
    amb_p = connection(amb, 'out1', pu, 'in1')
    p_sp = connection(pu, 'out1', sp, 'in1')
    sp_su = connection(sp, 'out1', su, 'in1')
    su_ev = connection(su, 'out1', ev, 'in1')
    ev_amb_out = connection(ev, 'out1', amb_out1, 'in1')
    nw.add_conns(amb_p, p_sp, sp_su, su_ev, ev_amb_out)

    # connection evaporator system - compressor system

    su_cp1 = connection(su, 'out2', cp1, 'in1')
    nw.add_conns(su_cp1)

    # compressor-system

    cp1_he = connection(cp1, 'out1', ic, 'in1')
    he_cp2 = connection(ic, 'out1', cp2, 'in1')
    cp2_c_out = connection(cp2, 'out1', cc, 'in1')
    sp_ic = connection(sp, 'out2', ic, 'in2')
    ic_out = connection(ic, 'out2', amb_out2, 'in1')
    nw.add_conns(cp1_he, he_cp2, sp_ic, ic_out, cp2_c_out)

    def __init__(self, q, eff, Temp):
        r"""
        :param Temp:
        :param q: q output
        :param eff: efficient of each part in pump
        """
        self.q = q
        self.eff = eff
        self.Temp = Temp

    def caculation(self):
        self.set_attr()

        HeatPump.nw.solve('design')
        P = [HeatPump.cp1.P.val, HeatPump.cp2.P.val, HeatPump.erp.P.val, HeatPump.pu.P.val]
        P_total = sum(map(abs, P))
        COP = self.q / P_total
        # T = [HeatPump.su_cp1.T.val, HeatPump.cp2_c_out.T.val, HeatPump.cd_ves.T.val, HeatPump.su_ev.T.val]
        # p = [HeatPump.su_cp1.p.val, HeatPump.cp2_c_out.p.val, HeatPump.cd_ves.p.val, HeatPump.su_ev.p.val,
        #      HeatPump.cp1_he.p.val]

        return P, P_total, COP

    def set_attr(self):
        r"""
        # %% set the attribution of the heat pump
        :return: heat output of the heat pump
        """

        HeatPump.cd.set_attr(pr1=0.99, pr2=0.99, ttd_u=15, design=['pr2', 'ttd_u'],
                             offdesign=['zeta2', 'kA'])
        HeatPump.dhp.set_attr(eta_s=self.eff, design=['eta_s'], offdesign=['eta_s_char'])
        HeatPump.cons.set_attr(pr=0.99, design=['pr'], offdesign=['zeta'])

        # water pump

        HeatPump.pu.set_attr(eta_s=self.eff, design=['eta_s'], offdesign=['eta_s_char'])

        # evaporator system

        kA_char1 = ldc('heat exchanger', 'kA_char1', 'DEFAULT', char_line)
        kA_char2 = ldc('heat exchanger', 'kA_char2', 'EVAPORATING FLUID', char_line)
        HeatPump.ev.set_attr(pr1=0.98, pr2=0.99, ttd_l=5,
                             kA_char1=kA_char1, kA_char2=kA_char2,
                             design=['pr1', 'ttd_l'], offdesign=['zeta1', 'kA'])

        HeatPump.su.set_attr(pr1=0.98, pr2=0.99, ttd_u=2, design=['pr1', 'pr2', 'ttd_u'],
                             offdesign=['zeta1', 'zeta2', 'kA'])

        HeatPump.erp.set_attr(eta_s=self.eff, design=['eta_s'], offdesign=['eta_s_char'])

        # compressor system

        HeatPump.cp1.set_attr(eta_s=self.eff, design=['eta_s'], offdesign=['eta_s_char'])
        HeatPump.cp2.set_attr(eta_s=self.eff, pr=3, design=['eta_s'], offdesign=['eta_s_char'])
        HeatPump.ic.set_attr(pr1=0.99, pr2=0.98, design=['pr1', 'pr2'],
                             offdesign=['zeta1', 'zeta2', 'kA'])

        # %% connection parametrization

        # condenser system

        HeatPump.c_in_cd.set_attr(fluid={'air': 0, 'NH3': 1, 'water': 0})
        HeatPump.cb_dhp.set_attr(T=20, p=10, fluid={'air': 0, 'NH3': 0, 'water': 1})
        HeatPump.cd_cons.set_attr(T=self.Temp)
        HeatPump.cons_cf.set_attr(h=ref(HeatPump.cb_dhp, 1, 0), p=ref(HeatPump.cb_dhp, 1, 0))

        # evaporator system cold side

        HeatPump.erp_ev.set_attr(m=ref(HeatPump.ves_dr, 1.25, 0), p0=5)
        HeatPump.su_cp1.set_attr(p0=5, h0=1700)

        # evaporator system hot side

        # pumping at constant rate in partload

        HeatPump.amb_p.set_attr(T=12, p=2, fluid={'air': 0, 'NH3': 0, 'water': 1},
                                offdesign=['v'])
        HeatPump.sp_su.set_attr(offdesign=['v'])
        HeatPump.ev_amb_out.set_attr(p=2, T=9, design=['T'])

        # compressor-system

        HeatPump.he_cp2.set_attr(Td_bp=5, p0=20, design=['Td_bp'])
        HeatPump.ic_out.set_attr(T=15, design=['T'])

        # %% key paramter

        HeatPump.cons.set_attr(Q=self.q)


def operation(state, last_q, last_state, method):
    r"""
    :param state: the gears of the heat pump --> int 0 - 3
    :param last_state: previous heat pump state --> int
    :param last_q: the heat output of last seconds --> float
    :param method: type of String, should be 'heater' or 'cooler' to indicate the type of heat pump
    :return: current heat output of the heat pump --> float
             power usage --> float
             the efficiency of the heat pump COP --> float
    """

    if method == 'Heater':
        k = 1
    elif method == 'Cooler':
        k = -1

    last_q = abs(last_q)
    total_state = 3
    current_q = state / total_state * 20000  # 20k aggregate capacity

    if abs(last_q - current_q) < 50:
        # if it is steady state return 1
        T = 20 * state / total_state
        steady = True
        last_q = current_q
    else:
        steady = False

    if last_state == 0:
        eff = 0.5
    else:
        eff = 0.87

    if last_q < current_q and not steady:
        if last_q == 0:
            T = 20
        else:
            T = math.ceil(40 * last_q / current_q) + 20
        Q_out = 0.004 * (current_q - last_q) + last_q

    elif last_q > current_q and not steady:
        T = 60 - 40 * last_q / current_q
        Q_out = -0.006 * (current_q - last_q) + last_q

    if eff < 0.87:
        eff += 0.0005
    elif eff > 0.5 and last_q > 15000:
        eff -= 0.0005

    elif state == 0:
        Q_out = 0
        T = 0
    print(Q_out, eff, T)
    hp = HeatPump(Q_out, eff, T)
    P, P_total, COP = hp.caculation()
    Q_out *= k

    return Q_out, P_total, COP


# example usage

if __name__ == '__main__':
    init = 0
    state = 1
    i = 0
    while 1:
        last_q = init
        Q, P_total, COP = operation(state, last_q, False, 'Heater')
        print(Q, P_total, COP)
        i += 1
        init = Q
        if i == 100:
            break


