import numpy as np
import matplotlib.pyplot as plt
from Wave_propogation_sim.py import Calc_E, Ef
import csv

#creates my constants
wavelenth = 800*10**-9
k = 2*np.pi/wavelenth
c = 2.9979e8
omega = c * k
tau = 5e-15
Emax = 1.0
x0 = -20e-6
dx = 20e-9
dt = 20*10**-18



# x array
x = np.arange(-25e-6,25e-6,dx)

# T array
t= np.arange(0, 1e-15, dt)


#initializes first 2 values of E
E0 = Calc_E(x,t[0])
E1 = Calc_E(x,t[1])
E1,E2,Et1i,Et2i = Ef(E0, E1, 1100)


#pointing vector
Si = []
for i in Et1i:
    Si.append((8.85418e-12)*(2.99e8)*(i**2))
En_i = 0
for i in Si:
    En_i += i*dt

# creates a figure and initializes the animation
fig, ax = plt.subplots()
ax.plot(x, E0, label="Initial")
ax.plot(x, E1, label="After 1100 steps")
#creates 2 dotted lines at -5e-6 and 5e-6 to signify the start and end of dielectric
ax.axvline(-5e-6, linestyle='--')
ax.axvline(5e-6, linestyle='--')
print(En_i)
E0 = Calc_E(x,t[0])
E1 = Calc_E(x,t[1])
E1,E2,Et1f,Et2f = Ef(E0, E1, 3200)
#pointing vector
Si1 = []
Si2 = []
for i in Et1f[1100:]:
    Si1.append((8.85418e-12)*(2.99e8)*(i**2))
for i in Et2f[1100:]:
    Si2.append((8.85418e-12)*(2.99e8)*(i**2))
ax.plot(x, E2, label="After 3000 steps")

En_i1 = 0
En_i2 =0
for i in range(len(Si1)):
    En_i1 += Si1[i]*dt
    En_i2 += Si2[i]*dt

print(En_i1+En_i2)


with open("E(t)Data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Initial E field", "Reflected", "Transmitted"])
    writer.writerows(zip(Et1i,Et1f,Et2f))

plt.legend()
plt.show()
