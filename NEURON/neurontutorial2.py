from neuron import h, gui
soma = h.Section(name='soma')
h.psection() # prints information about the cell
#dir(soma) # shows all attributes of the cell 'soma'

dend = h.Section(name='dend')
h.psection(sec=dend)
h.topology() # shows connection diagram

# Surface area of cylinder is 2*pi*r*h (sealed ends are implicit).
# Here we make a square cylinder in that the diameter
# is equal to the height, so diam = h. ==> Area = 4*pi*r^2
# We want a soma of 500 microns squared:
# r^2 = 500/(4*pi) ==> r = 6.2078, diam = 12.6157
soma.L = soma.diam = 12.6157 # Makes a soma of 500 microns squared.
dend.L = 180 # microns
dend.diam = 1 # microns
dend.nseg = 11 # odd number of segments

soma_area = h.area(0.5, sec=soma)
print("Surface area of soma = {}".format(soma_area,))

# Iterate over all sections
for sec in h.allsec():
    sec.Ra = 100 # Axial resistance in Ohm * cm
    sec.cm = 1 # Membrane capacitance in micro Farads / cm^2

# Insert active Hodgkin-Huxley current in the soma
soma.insert('hh')
# Insert passive leak current in dendrite
dend.insert('pas')

print(dend(0.5).pas.g)
print(dend(0.5).g_pas)
mech = dend(0.5).pas
print(dir(mech))
print(mech.g)

dend.g_pas = 0.001
print(dend(0.1).pas.g)
print(dend(0.9).pas.g)

soma.gnabar_hh = 0.12 # Sodium conductance in S/cm2
soma.gkbar_hh = 0.036 # Potassium conductance in S/cm2
soma.gl_hh = 0.0003 # Leak conductance in S/cm2
soma.el_hh = -54.3 # Reversal potential in mV # Insert passive current in the dendrite
dend.g_pas = 0.001 # Passive conductance in S/cm2
dend.e_pas = -65 # Leak reversal potential mV

stim = h.IClamp(dend(1.0))

dir(stim)
stim.amp = 0.1 # input current in nA
stim.delay = 20 # turn on after this time in ms
stim.dur = 3 # duration in ms

v_vec = h.Vector()
v_vec_soma = h.Vector() # Membrane potential vector
v_vec_dend = h.Vector() # Membrane potential vector
t_vec = h.Vector() # Time stamp vector
# v_vec.record(h._ref_v)
v_vec_soma.record(soma(0.5)._ref_v)
v_vec_dend.record(dend(1.0)._ref_v)
t_vec.record(h._ref_t)

h.tstop = 40.0
h.run()

shape_window = h.PlotShape()
shape_window.exec_menu('Show Diam')

from matplotlib import pyplot as plt
plt.ion()
plt.figure(figsize=(8,4)) # Default figsize is (8,6)
# plt.plot(t_vec, v_vec)
plt.plot(t_vec, v_vec_soma, 'b', label='soma')
plt.plot(t_vec, v_vec_dend, 'r', label='dend')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.legend()
plt.show()
