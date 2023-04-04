import numpy as np
import matplotlib.pyplot as plt
from Q3 import ODE, nODE

class VanDerPolEqn(nODE):
    
    class velocity(ODE):
        
        def __init__(self, initial_value, mu, x : ODE):
            self.mu = mu
            self.x = x

            super().__init__(initial_value)

        def forward_euler(self, h):
            self.value += (self.mu*(1-(self.x())**2)*self.value - self.x())*h

    class position(ODE):
        
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



if __name__ == '__main__':
    x0 = 1
    v0 = 0
    mu = 0.7
    

    duration = 50
    dt = 0.01

    plt.title("x vs t")
    oscillator = VanDerPolEqn(x0, v0, 1)
    oscillator.Plot(duration, dt, plot_params=[('t', 'x', '1')])
    oscillator = VanDerPolEqn(x0, v0, 10)
    oscillator.Plot(duration, dt, plot_params=[('t', 'x', '10')])
    oscillator = VanDerPolEqn(x0, v0, 20)
    oscillator.Plot(duration, dt, plot_params=[('t', 'x', '20')])
    plt.legend()
    plt.show()

    plt.title("v vs t")
    oscillator = VanDerPolEqn(x0, v0, 1)
    oscillator.Plot(duration, dt, plot_params=[('t', 'v', '1')])
    oscillator = VanDerPolEqn(x0, v0, 10)
    oscillator.Plot(duration, dt, plot_params=[('t', 'v', '10')])
    oscillator = VanDerPolEqn(x0, v0, 20)
    oscillator.Plot(duration, dt, plot_params=[('t', 'v', '20')])
    plt.legend()
    plt.show()

    plt.title("x vs v")
    oscillator = VanDerPolEqn(x0, v0, 1)
    oscillator.Plot(duration, dt, plot_params=[('x', 'v', '1')])
    oscillator = VanDerPolEqn(x0, v0, 10)
    oscillator.Plot(duration, dt, plot_params=[('x', 'v', '10')])
    oscillator = VanDerPolEqn(x0, v0, 20)
    oscillator.Plot(duration, dt, plot_params=[('x', 'v', '20')])
    plt.legend()
    plt.show()
