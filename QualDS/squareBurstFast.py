# coding: utf-8
import xppy
from xppy.utils import plot
xppy.set_cmd('~/xppaut8.0ubuntu/')

odefile = 'square_burst_fast.ode'
def run_file():
	squareBurst=xppy.run(odefile)
	return squareBurst

squareBurst = run_file()
squareBurst.getDesc()
sBData=squareBurst.getRawData()
sBData.shape

import numpy as np
for I in np.linspace(0, 50, 100):
	xppy.changeOde(["param I=%f" % (I,)], odefile)
	with open(odefile, 'r') as odf:
		print('\n'.join(odf.readlines()))
	squareBurst = run_file()
	plot.plotLC(squareBurst.getRawData())
	plot.pl.show()
