import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#creates my constants
wavelenth = 800*10**-9
k = 2*np.pi/wavelenth
c = 2.9979e8
omega = c * k
tau = 5e-15
Emax = 1.0
x0 = -15e-6
dx = 20e-9
dt = 20*10**-18



# x array
x = np.arange(-20e-6,20e-6,dx)

v = x.copy()*0
for i in range(len(v)):
    if x[i] > -5e-6 and x[i] < 5e-6:
        v[i]= 2.9979e8/1.5
    else:
        v[i]= 2.9979e8


# T array
t= np.arange(0, 1e-15, dt)


def Calc_E(x,t):
    #uses the E function to create 2 initial values for E
    u0 = omega * tau
    u = []
    for xi in x:
        u.append(k*(xi-x0) - omega*t)
    E= []
    for ui in u:
        E.append(Emax * np.e**(- (ui/u0)**2 ) * np.cos(ui))

    return E

def Ef(E0,E1, optimizer = 1):
    '''Uses 4th order finite differencing to calculate future values of E'''
    for opt in range(optimizer):
        E2 = [0,0]
        for i in range(2,len(E1[:-2])):
            E2.append((((v[i]**2)*(-E1[i+2]+(16*E1[i+1])-30*E1[i]+16*E1[i-1]-E1[i-2])*(dt**2)/(12*(dx**2)))+2*E1[i])-E0[i])
        #appends 2 dummy values to list to accound for losing 2 values with 4th order finite differencing
        E2.extend([0,0])

        E0 = E1.copy()
        E1 = E2.copy()

    return E0,E1

#initializes first 2 values of E
E0 = Calc_E(x,t[0])
E1 = Calc_E(x,t[1])

# creates a figure and initializes the animation
fig, ax = plt.subplots()
line, = ax.plot(x, E1)

#creates 2 dotted lines at -5e-6 and 5e-6 to signify the start and end of dielectric
ax.axvline(-5e-6, linestyle='--')
ax.axvline(5e-6, linestyle='--')

#marks the boundaries for the animation
ax.set_xlim(x.min(), x.max())
ax.set_ylim(-1.2, 1.2)


def update(frame):
    ''' update function (Game Loop) that continuously gets called to produce a future value for E updating'''
    global E0, E1

    E1,E2 = Ef(E0, E1, 10)

    E0 = E1.copy()
    E1 = E2.copy()

    line.set_ydata(E2)
    return line,

ani = FuncAnimation(
    fig,
    update, 
    frames=650, 
    interval=1, 
    blit=True
)

ani.save("wave_animation.gif", writer="pillow", fps=45)
