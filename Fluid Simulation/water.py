from simulator import Simulator
import sys

def ext(fluid):
    fluid.apply_gravity()
    fluid.add_density(fluid.solver.N/2, fluid.solver.N/4, 1000)

def density_color(sim, i, j):
    col = round(sim.fluid.get_density()[i,j]*255/10)
    col = max(0, min(255,col))
    v_x, v_y = sim.fluid.get_velocity(i,j)
    mod = abs(v_x + v_y)
    col1 = int(min(255, col*(mod/2)))
    return (col1, col1, col)


if __name__ == '__main__':

    if len(sys.argv) == 7:
        N = int(sys.argv[1])
        resolution = int(sys.argv[2])
        force = int(sys.argv[3])
        source = int(sys.argv[4])
        diff = float(sys.argv[5])
        visc = float(sys.argv[6])

        sim = Simulator(N, resolution, force, source, diff, visc, True)


    else:
        print("Invalid input format. Please enter 6 arguments: N (int), resolution (int), force (int), source (int), diff (float), and visc (float) separated by spaces.")
        print("Running using standard values")
        print("64 20 70 1000 0.0 0.0")

        sim = Simulator(N=64, resolution=20, force = 70, source=1000, diff = 0.0, visc = 0.0, isWaterSim=True)


    sim.fluid.ext_update = lambda : ext(sim.fluid)
    sim.density_color = lambda i,j: density_color(sim, i, j)

    sim.Start()

    