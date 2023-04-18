import matplotlib.pyplot as plt

class ODE:
    """
    Represents a single ODE. Includes initial value, euler method function definition and is updatable.
    Abstract class.

    forward_euler : Updation function using forward Euler method.
    backward_euler : Updation function using backward Euler method.
    Both takes input the class and the value of h
    ie. forward_euler(self, h) updates the value of x and t in the current step of the ODE.
    """

    def __init__(self, initial_value):
        # Abstraction
        self.initial_value = initial_value
        self.value = initial_value

    def __call__(self):
        return self.value

    def reset(self):
        self.value = self.initial_value

class nODE:
    """
    Represents an n-order ODE. Saved as n single order ODEs.
    Abstract class.
    
    _ODEs = {variable name : ODE}
    """

    def __init__(self, **kwargs):
        # This may need to be rephrased to allow interdependant equations
        self._ODEs = kwargs

    def forward_update(self, h):
        for ode in self._ODEs.values():
            ode.forward_euler(h)

    def backward_update(self, h):
        for ode in self._ODEs.values():
            ode.backward_euler(h)

    def get_variable(self, var):
        return self._ODEs[var]()
    
    def reset(self):
        for ode in self._ODEs.values():
            ode.reset()

    def Plot(self, t_final, h, plot_params):
        """
        Function to plot ODEs. plot_params is a list of tuples of (x,y) where x and y are the names of the variables which are to be plotted against each other.
        (x,y, label) can be used to label a plot.
        """
        t = 0
        T = [t]
        vals = {x: [self.get_variable(x)] for x in self._ODEs}

        while t<t_final:
            self.forward_update(h)

            t += h
            T.append(t)

            for x in vals:
                vals[x].append(self.get_variable(x))

        vals['t'] = T
        
        for plot_param in plot_params:
            try:
                x,y, label = plot_param
                plt.plot(vals[x], vals[y], label=label)
            except ValueError as e:
                x,y = plot_param
                plt.plot(vals[x], vals[y])

        # Reset values to initial values after plotting.
        self.reset()