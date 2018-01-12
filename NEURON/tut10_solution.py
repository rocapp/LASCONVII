from neuron import h, gui
from matplotlib import pyplot
import numpy as np

# PART 1: Passive propagation in unmyelinated axon

soma = h.Section(name='soma')
axon = h.Section(name='axon')
axon.connect(soma(1))

# Surface area of cylinder is 2*pi*r*h (sealed ends are implicit).
soma.L = soma.diam = 12.6157 # Makes a soma of 500 microns squared.
axon.L = 10000 # microns (1cm)
axon.diam = 1  # microns

for sec in h.allsec():
    sec.Ra = 100    # Axial resistance in Ohm * cm
    sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
    
# Insert active Hodgkin-Huxley current in the soma
soma.insert('hh')
soma.gnabar_hh = 0.12  # Sodium conductance in S/cm2
soma.gkbar_hh = 0.036  # Potassium conductance in S/cm2
soma.gl_hh = 0.0003    # Leak conductance in S/cm2
soma.el_hh = -54.3     # Reversal potential in mV

# Insert passive current in the axon
axon.insert('pas')
axon.g_pas = 0.001  # Passive conductance in S/cm2
axon.e_pas = -65    # Leak reversal potential mV
axon.nseg = 1000

#Insert current clamp on 1 position of soma
stim = h.IClamp(soma(1))
stim.delay = 5
stim.dur = 1
stim.amp = 1

#set up plot
t_vec = h.Vector()  # record time
t_vec.record(h._ref_t)

v_vec_soma = h.Vector() # record soma
v_vec_soma.record(soma(1.0)._ref_v)

axon_locs = np.arange(0,0.1,0.01)  # set axon recording times
v_vec_axon=[]
for loc in axon_locs:
    v_vec_axon.append(h.Vector())
    v_vec_axon[-1].record(axon(loc)._ref_v)
    
## run simulation (passive propagation in axon)
h.tstop = 30
h.run()

#pyplot format
pyplot.figure(figsize = (8,4))
pyplot.plot(t_vec, v_vec_soma, label = 'soma')  # plot soma
for i,v_vec in enumerate(v_vec_axon):  # plot axon
    pyplot.plot(t_vec, v_vec, label = 'axon '+str(axon_locs[i]))
pyplot.legend()
pyplot.xlabel('time (ms)')
pyplot.ylabel('mV')
# pyplot.show()


# PART 2: active propagation in unmyelinated axon
#add HH in axon
axon.insert('hh')
axon.gnabar_hh = 0.3  # Sodium conductance in S/cm2, gnabar_hh higher than thi
axon.gkbar_hh = 0.036   # Creates a latchup condition 
axon.gl_hh = 0.0003    
axon.el_hh = -54.3 

##set up plot
t_vec = h.Vector()  # record time
t_vec.record(h._ref_t)

v_vec_soma = h.Vector() # record soma
v_vec_soma.record(soma(1.0)._ref_v)

axon_locs = np.arange(0, 1.0, 0.1)  # set axon recording times
v_vec_axon=[]
for loc in axon_locs:
    v_vec_axon.append(h.Vector())
    v_vec_axon[-1].record(axon(loc)._ref_v)
    
#set up sim duration
simdur = 40
h.tstop = simdur
h.run()

#pyplot format
pyplot.figure(figsize = (8,4))
pyplot.plot(t_vec, v_vec_soma, label = 'soma')  # plot soma
for i,v_vec in enumerate(v_vec_axon):  # plot axon
    pyplot.plot(t_vec, v_vec, label = 'axon '+str(axon_locs[i]))
pyplot.legend()
pyplot.xlabel('time (ms)')
pyplot.ylabel('mV')
# pyplot.show()


# PART 3: active propagation in myelinated axon (with nodes of ranvier)
ranvierNodeInterval = 1000

axon.nseg = 10000  # each segment = 10um

# Set active conductances for all segements to 0 (close all active channels)
axon.gnabar_hh = 0  
axon.gkbar_hh = 0   
axon.gl_hh = 0
axon.g_pas = 0.000001
axon.cm = 0.00001

for segIndex in range(1, axon.nseg, ranvierNodeInterval):
    segIndexNorm = float(segIndex)/float(axon.nseg)    
    axon(segIndexNorm).hh.gnabar = 0.3
    axon(segIndexNorm).hh.gkbar = 0.036
    axon(segIndexNorm).hh.gl = 0.0003 
    axon(segIndexNorm).pas.g = 0.001 
    axon(segIndexNorm).cm = 3
    
##set up plot
t_vec = h.Vector()  # record time
t_vec.record(h._ref_t)

v_vec_soma = h.Vector() # record soma
v_vec_soma.record(soma(1.0)._ref_v)

axon_locs = np.arange(0, 1, 0.1)  # set axon recording times
v_vec_axon=[]
for loc in axon_locs:
    v_vec_axon.append(h.Vector())
    v_vec_axon[-1].record(axon(loc)._ref_v)
    
#set up sim duration
simdur = 40
h.tstop = simdur
h.run()

#pyplot format
pyplot.figure(figsize = (8,4))
pyplot.plot(t_vec, v_vec_soma, label = 'soma')  # plot soma
for i,v_vec in enumerate(v_vec_axon):  # plot axon
    pyplot.plot(t_vec, v_vec, label = 'axon '+str(axon_locs[i]))
pyplot.legend()
pyplot.xlabel('time (ms)')
pyplot.ylabel('mV')
pyplot.show()
