import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

nsteps = 1000

t = np.linspace(0, 100, nsteps)

I = 2.
tau = 0.1
thresh = 1.
reset = -1.
v0 = 0.

def dV(vt,ti):
    return -(vt-I)/tau

v = np.zeros(nsteps)
dt = 0.001
for i in range(len(t)-1):
    dvdt = dV(v[i],t[i],)
    vv = v[i] + dvdt*dt
    if vv > thresh:
        v[i + 1] = reset
    else:
        v[i + 1] = vv
    print(v[i+1])

plt.figure()
plt.plot(t, v)

plt.figure()
plt.plot(t, np.exp(t/tau)*(I-v))
plt.show()
