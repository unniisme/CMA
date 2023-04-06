import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from Q3 import ODE, nODE

class VanDerPolEqn(nODE):
    
    class velocity(ODE):
        """
        dv/dt - μ(1-x²)*v + x = 0
        Where v and x are functions of t

        Forward updation:
        v(t+1) = v(t) + (μ(1-x(t)²)*v(t) - x(t))*h
        """
        
        def __init__(self, initial_value, mu, x : ODE):
            self.mu = mu
            self.x = x

            super().__init__(initial_value)

        def forward_euler(self, h):
            self.value += (self.mu*(1-(self.x())**2)*self.value - self.x())*h

    class position(ODE):
        """
        dx/dt = v
        Where v and x are functions of t

        Forward (and infact backward!) updation:
        x(t+1) = x(t) + v(t)*h
        """
        
        def __init__(self, initial_value, v:ODE):
            self.v = v

            super().__init__(initial_value)

        def forward_euler(self, h):
            self.value += self.v()*h


    def __init__(self, x0, v0, mu):
        x = VanDerPolEqn.position(x0, None) #Velocity ODE updated separately
        v = VanDerPolEqn.velocity(v0, mu, x)

        x.v = v

        super().__init__(x = x, v = v)


def FindFrequency(mu, x0, v0):
    dt = 0.0001
    t = 0

    oscillator = VanDerPolEqn(x0, v0, mu)

    # Limit cycle is the time between 2 global maximas
    # Average over 5 limit cycles is taken
    upSlope = True
    limitCycles=[]
    X = []
    T = []
    lastExtrema = 0

    oldx = oscillator.get_variable('x')

    while len(limitCycles) < 7:
        oscillator.forward_update(dt)
        X.append(oscillator.get_variable('x'))
        T.append(t)
        if oldx > oscillator.get_variable('x') and upSlope:
            limitCycles.append(t-lastExtrema)
            lastExtrema = t

        upSlope = oldx < oscillator.get_variable('x')

        t += dt

    limitCycles.pop(0) #Remove first measure as it is simply the time from start to first maxima
        
    print(f"mu = {mu}\t Limit cycle = {sum(limitCycles)/len(limitCycles)}")

    plt.title("Van der Pol Oscillator with μ = " + str(mu))
    plt.xlabel("time")
    plt.ylabel("x")
    plt.plot(T,X)
    endpoints = (lastExtrema, lastExtrema-limitCycles[-1])
    plt.plot(endpoints, np.interp(endpoints, T, X))

    plt.show()

    return sum(limitCycles)/len(limitCycles)




if __name__ == '__main__':
    
    FindFrequency(0.01,1,0.1)
    FindFrequency(0.1,1,-0.3)
    FindFrequency(1,0.1,0.2)
    FindFrequency(4,-0.4,1)
    FindFrequency(10,-0.4,1)