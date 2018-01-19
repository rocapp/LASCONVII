from neuron import h, gui
from matplotlib import pyplot
import numpy as np

# PART 1: Active propagation Myelinated axon

for aL in np.arange(10000,30000,2000):

	somaMotor = h.Section(name='somaMotor')
	somaMotor.L = somaMotor.diam = 12.6157 # microns

	axonMotor = h.Section(name='axonMotor')
	axonMotor.L = aL #30000 # microns
	axonMotor.diam = 1 #microns
	segmentSize = 50 # microns
	axonMotor.nseg = int(aL / 2.0) #15000 # axonMotor.L/segmentSize

	axonMotor.connect(somaMotor(1))

	for sec in h.allsec():
		sec.Ra = 100    # Axial resistance in Ohm * cm
		sec.cm = 1      # Membrane capacitance in micro Farads / cm^2

	# print "Show the connection topology"
	# print h.topology()

	# Insert active Hodgkin-Huxley current in the soma
	somaMotor.insert('hh')
	somaMotor.gnabar_hh = 0.12  # Sodium conductance in S/cm2
	somaMotor.gkbar_hh = 0.036  # Potassium conductance in S/cm2
	somaMotor.gl_hh = 0.0003    # Leak conductance in S/cm2
	somaMotor.el_hh = -65 # -54.3    # Reversal potential in mV

	# Adding active HH channels in the Axon of the passive Neuron
	axonMotor.insert('hh')
	# axonMotor.gnabar_hh = 0.0  # Sodium conductance in S/cm2
	# axonMotor.gkbar_hh = 0.0  # Potassium conductance in S/cm2
	# axonMotor.gl_hh = 0.0    # Leak conductance in S/cm2
	# axonMotor.cm = 0.01

	ranvierNodeInterval = 1 # segmentSize/1000 # interval to place Nodes of Ranvier (in um)

	for segIndex in range(1, axonMotor.nseg):#, ranvierNodeInterval):
		segIndexNorm = float(segIndex)/float(axonMotor.nseg)
		
		if segIndex % 25.0 == 0:
			print segIndex
			# print 'Okay!!'# statement(s)
			# print (np.exp(-2*segIndex/axonMotor.nseg))*0.3

			axonMotor(segIndexNorm).hh.gnabar = 0.12
			axonMotor(segIndexNorm).hh.gkbar = 0.036
			axonMotor(segIndexNorm).hh.gl = 0.0003
			# axonMotor(segIndexNorm).pas.g = 0.001
			axonMotor(segIndexNorm).cm = 5

		# 	axonMotor(segIndexNorm).hh.gnabar = (np.exp(-2*segIndex/axonMotor.nseg))*0.3
		# 	print (1-np.exp(-2*segIndex/axonMotor.nseg))*0.3
		# 	axonMotor(segIndexNorm).cm = (np.exp(-2*segIndex/axonMotor.nseg))*3
		else:
			axonMotor(segIndexNorm).hh.gnabar 	= 0.0  # Sodium conductance in S/cm2
			axonMotor(segIndexNorm).hh.gkbar 	= 0.0  # Potassium conductance in S/cm2
			axonMotor(segIndexNorm).hh.gl 		= 0.0    # Leak conductance in S/cm2
			axonMotor(segIndexNorm).cm = 0.01

			# exponentialScaling = (np.exp(-5*(1-segIndexNorm)))
			# # print exponentialScaling*0.12		
			# channelScaling = 0.1
			# axonMotor(segIndexNorm).hh.gnabar 	= exponentialScaling* 0.12*channelScaling # 0.0  # Sodium conductance in S/cm2
			# axonMotor(segIndexNorm).hh.gkbar 	= exponentialScaling* 0.036*channelScaling # 0.0  # Potassium conductance in S/cm2
			# axonMotor(segIndexNorm).hh.gl 		= exponentialScaling*0.0003 # 0.0    # Leak conductance in S/cm2
			# axonMotor(segIndexNorm).cm 			= 0.01+exponentialScaling*(5-0.01)

	# #Insert current clamp on 1 position of soma
	# stim = h.IClamp(somaMotor(0))
	# stim.delay = 5
	# stim.dur = 1
	# stim.amp = 1

	# stim1 = h.IClamp(somaMotor(0))
	# stim1.delay = 55
	# stim1.dur = 1
	# stim1.amp = 1

	# stim2 = h.IClamp(somaMotor(0))
	# stim2.delay = 105
	# stim2.dur = 1
	# stim2.amp = 1

	# axonMotor.insert('pas')
	# # print h.psection(sec=axonMotor(0.5))
	# axonMotor(0.5).g_pas = 0.001

	# Insert Alpha Synapse
	syn = h.AlphaSynapse(somaMotor(1.0))
	syn.e = 0  # equilibrium potential in mV
	# syn.onset = 20  # turn on after this time in ms
	syn.gmax = 0.1  # set conductance in uS
	syn.tau = 0.1 # set time constant 

	#set up plot
	t_vec = h.Vector()  # record time
	t_vec.record(h._ref_t)

	v_vec_soma = h.Vector() # record soma
	v_vec_soma.record(somaMotor(0.5)._ref_v)

	# Setting up the recordings
	axon_locs = np.arange(0.05,1,0.001)  # set axon recording times
	v_vec_axon=[]
	for loc in axon_locs:
	    v_vec_axon.append(h.Vector())
	    v_vec_axon[-1].record(axonMotor(loc)._ref_v)
	    
	## run simulation (passive propagation in axon)

	#h.topology()

	h.tstop = 75
	h.run()

	#pyplot format
	pyplot.figure(figsize = (8,4))
	pyplot.plot(t_vec, v_vec_soma, label = 'sM')  # plot soma
	for i,v_vec in enumerate(v_vec_axon):  # plot axon
	    pyplot.plot(t_vec, v_vec, label = 'aM '+str(axon_locs[i]))
	pyplot.legend()
	pyplot.title('Degraded Axon - Stage 3 [10 cm]')
	pyplot.xlabel('time (ms)')
	pyplot.ylabel('mV')
	pyplot.savefig('figs\\axonLen_%d.png' % (aL,))
	pyplot.close('all')
	#pyplot.show()