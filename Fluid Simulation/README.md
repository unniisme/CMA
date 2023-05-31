# Navier Stokes Simulator
A fluid simulator using Python and Numpy.  
Visualizations are using pygame.

### `NavierStokes.py`
Contains code on fluid simulation in the fluid solver class.  
For more information on exact implementational code, visit [reference](#references)  
There are also wrapper funtions for holding simulational data.

### `simulator.py`
Pygame wrapper code for running an interactive simulation.

### `smoke.py`
A smoke simulator in pygame.

### `water.py`
A supposed water simulation in pygame. 
Does not work properly as water requires simulation of surface tension, incompressability among other things to behave realistically.

### `text_simulator.py`
A demo of the program that runs fully in CLI. Does not require pygame. Not interactive either.
```bash
$ clear
$ python3 text_simulator.py
(To close : $ ^C)
$ clear
```
Clears are because it messes up stdout otherwise