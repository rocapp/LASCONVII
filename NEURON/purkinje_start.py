'''* Purkinje19b972 current clamp simulation: sample traces of somatic  */
/* and dendritic epsps                                                */
/* synapse at "dend2" (dendA1_001011(1))                              */
/* Michael Hausser and Arnd Roth                                      */
/* Version 1.2 for LASCON 2014                              14.1.2014 */
'''
from neuron import h,gui
from matplotlib import pyplot as plt
import numpy as np

# initial parameters 
t = 0                   # simulation starts at t = 0 ms */
dt = 0.01               # time step, ms */
Vrest = -70             # resting potential, mV */

h.load_file("Purkinje19b972-1.nrn")  # load the morphology file */

shape_window = h.PlotShape()
shape_window.exec_menu('Show Diam')

# membrane properties are defined here */
membranecap = 0.638856    # specific membrane capacitance in uF cm^-2 */
membraneresist = 120236.0 # specific membrane resistance in ohm cm^2 */
axialresist = 141.949     # axial resistivity in ohm cm */

# all sections
allsec = h.allsec()
for sec in h.allsec():
	sec.insert('pas')
	sec.e_pas=Vrest

# dend sections
dend = [s for s in allsec if s.name().startswith('dend')]
for sec in dend:
	sec.g_pas = 5.34/membraneresist
	sec.Ra = axialresist
	sec.cm = 5.34*membranecap

# dendA1_0 sections
dendA1_list = ['dendA1_0', 'dendA1_00', 'dendA1_001', 'dendA1_0010', 'dendA1_00101', 'dendA1_001011', 
	'dendA1_0010110', 'dendA1_0010111', 'dendA1_00101110', 'dendA1_001011101', 'dendA1_00101111', 'dendA1_001011110' 
	'dendA1_0010111101',  'dendA1_00101111011', 'dendA1_0011', 'dendA1_00110', 'dendA1_001101', 'dendA1_0011010', 
	'dendA1_0011011', 'dendA1_00110110', 'dendA1_01', 'dendA1_010', 'dendA1_011', 'dendA1_0100', 'dendA1_0101'
	'dendA1_01001', 'dendA1_010010', 'dendA1_0100100', 'dendA1_01001001', 'dendA1_010010010']
dendA1 = [s for s in allsec if s.name() in dendA1_list]
for sec in dendA1:
	sec.g_pas = 1.2/membraneresist
	sec.Ra = axialresist
	sec.cm = 1.2*membranecap

# soma sections
soma = [s for s in allsec if s.name().startswith('soma')]
for sec in soma:
	sec.g_pas = 1.0/membraneresist
	sec.Ra = axialresist
	sec.cm = 1.0*membranecap

# axon sections
axon = [s for s in allsec if s.name().startswith('axon')]
for sec in axon:
	sec.g_pas = 1.0/membraneresist
	sec.Ra = axialresist
	sec.cm = 1.0*membranecap

# some axonA1 sections
axonA1_list = ['axonA1_0', 'axonA1_000', 'axonA1_0000', 'axonA1_0001', 'axonA1_01', 'axonA1_010']
axonA1 = [s for s in allsec if s in axonA1_list]
for sec in axonA1:
	sec.g_pas = 0.1/membraneresist
	sec.Ra = axialresist
	sec.cm = 0.1*membranecap

# Add current clamp with duration 0.5ms, 1nA amplitude at somaA(0.5)
stim_ = True
if stim_:
        stim = h.IClamp(h.somaA(0.5))
        stim.amp = 1 # nA
        stim.dur = 0.5 # ms

# record soma voltage and time
t_vec = h.Vector()
v_vec_soma = h.Vector()
v_vec_dend = h.Vector()
v_vec_soma.record(h.somaA(0.5)._ref_v) # change recoding pos
v_vec_dend.record(h.dendA1_01001(0.7)._ref_v)
t_vec.record(h._ref_t)

# run simulation
h.tstop = 100 # ms
h.v_init = Vrest
h.run()  


# plot voltage vs time
plt.figure(figsize=(8,4)) # Default figsize is (8,6)
plt.semilogy(t_vec, v_vec_soma.abs(), 'b', label='soma')
plt.semilogy(t_vec, v_vec_dend.abs(), 'r', label='dend')
plt.xlabel('time (ms)')
plt.ylabel('log mV')
plt.legend()
plt.show()

