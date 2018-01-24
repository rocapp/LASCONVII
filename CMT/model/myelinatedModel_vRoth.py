import os
from neuron import h, gui
from matplotlib import pyplot
import numpy as np

for aL in np.arange(7000,21000,2000):

	''' PART 1
	Here we created a Neuron with 	a soma and an axon component
	somaMotor is a sphere
	axonMotor is a cylinder with 	length of 1 meter (10^6 microns)
									segments of 2 microns each
									each myelin sheet has a length of 48 microns
									each ranvier node has a length of 02 microns
	'''
	# Creating the Soma structure
	somaMotor = h.Section(name='somaMotor')
	somaMotor.L = somaMotor.diam = 12.6157 # microns

	# Creating the Axon structure
	axonMotor = h.Section(name='axonMotor')
	axonMotor.L = aL # microns
	axonMotor.diam = 1. #microns
	segmentSize = 2 # microns
	print axonMotor.L/segmentSize
	axonMotor.nseg = int(int(axonMotor.L) / int(segmentSize)) #15000 # axonMotor.L/segmentSize

	# Connecting the Soma and Axon
	axonMotor.connect(somaMotor(1))

	# Changing the cell membrane resistance
	for sec in h.allsec():
		sec.Ra = 100    # Axial resistance in Ohm * cm
		sec.cm = 1      # Membrane capacitance in micro Farads / cm^2

	# Inserting active Hodgkin-Huxley current in the soma
	somaMotor.insert('hh')
	somaMotor.gnabar_hh = 0.12  # Sodium conductance in S/cm2
	somaMotor.gkbar_hh = 0.036  # Potassium conductance in S/cm2
	somaMotor.gl_hh = 0.0003    # Leak conductance in S/cm2
	somaMotor.el_hh = -65 # -54.3    # Reversal potential in mV

	# Adding active HH channels in the Axon of the passive Neuron
	axonMotor.insert('hh')

	for segIndex in range(1, axonMotor.nseg):
		segIndexNorm = float(segIndex)/float(axonMotor.nseg)
		
		if segIndex % 25.0 == 0:						# Ranvier Node membrane properties
			print segIndex
			axonMotor(segIndexNorm).hh.gnabar = 0.12
			axonMotor(segIndexNorm).hh.gkbar = 0.036
			axonMotor(segIndexNorm).hh.gl = 0.0003
			axonMotor(segIndexNorm).cm = 5.

		else:											# Myelin Sheat membrane properties

			axonMotor(segIndexNorm).hh.gnabar 	= 0.0  	# Sodium conductance in S/cm2
			axonMotor(segIndexNorm).hh.gkbar 	= 0.0  	# Potassium conductance in S/cm2
			axonMotor(segIndexNorm).hh.gl 		= 0.0   # Leak conductance in S/cm2
			axonMotor(segIndexNorm).cm = 0.01
			'''	
				This section creates an exponential degradation in the myelin sheat, 
				by increasing the capacitance from the soma to the tip of the axon,
				in order to mimic demyelination, but we are going to change it for another model later on
			'''

			# exponentialScaling = (np.exp(-5*(1-segIndexNorm)))
			# # print exponentialScaling*0.12		
			# channelScaling = 0.1
			# axonMotor(segIndexNorm).hh.gnabar 	= exponentialScaling* 0.12*channelScaling # 0.0  # Sodium conductance in S/cm2
			# axonMotor(segIndexNorm).hh.gkbar 		= exponentialScaling* 0.036*channelScaling # 0.0  # Potassium conductance in S/cm2
			# axonMotor(segIndexNorm).hh.gl 		= exponentialScaling*0.0003 # 0.0    # Leak conductance in S/cm2
			# axonMotor(segIndexNorm).cm 			= 0.01+exponentialScaling*(5-0.01)

	# Insert current clamp on 1 position of soma
	'''	
		We tried current clamp, but it worked as same as the Alpha Synapse
	'''
	# stim = h.IClamp(somaMotor(0))
	# stim.delay = 5
	# stim.dur = 1
	# stim.amp = 1

	# Insert Alpha Synapse
	syn = h.AlphaSynapse(somaMotor(1.0))
	syn.e = 0  # equilibrium potential in mV
	# syn.onset = 20  # turn on after this time in ms
	syn.gmax = 0.1  # set conductance in uS
	syn.tau = 0.1 # set time constant 

	# Set up plot
	t_vec = h.Vector()  # record time
	t_vec.record(h._ref_t)

	v_vec_soma = h.Vector() # record soma
	v_vec_soma.record(somaMotor(0.5)._ref_v)

	# Setting up the recordings
	axon_locs = np.arange(0.001,1,0.001)  # set axon recording times
	v_vec_axon=[]
	for loc in axon_locs:
	    v_vec_axon.append(h.Vector())
	    v_vec_axon[-1].record(axonMotor(loc)._ref_v)
	    
	## run simulation (passive propagation in axon)
	# h.topology()
	h.tstop = 500
	h.run()

	#pyplot format
	pyplot.figure(figsize = (8,4))
	pyplot.plot(t_vec, v_vec_soma, label = 'sM')  # plot soma
	for i,v_vec in enumerate(v_vec_axon):  # plot axon
	    pyplot.plot(t_vec, v_vec, label = 'aM '+str(axon_locs[i]))
	pyplot.legend()
	pyplot.title('Myelinated Axon: Axon Length: %d microns' % (aL,))
	pyplot.xlabel('time (ms)')
	pyplot.ylabel('mV')
	pyplot.savefig('figs'+os.sep+'axonLen_%03d.png' % (aL,))
	pyplot.close('all')
	# pyplot.show()
	
