from simulator import Simulator
import sys

if __name__ == '__main__':

    if len(sys.argv) == 8:
        N = int(sys.argv[1])
        resolution = int(sys.argv[2])
        force = int(sys.argv[3])
        source = int(sys.argv[4])
        diff = float(sys.argv[5])
        visc = float(sys.argv[6])
        temp_diff = float(sys.argv[7])

        sim = Simulator(N, resolution, force, source, diff, visc, temp_diff)


    else:
        print("Invalid input format. Please enter 6 arguments: N (int), resolution (int), force (int), source (int), diffusion coefficient (float), visc (float) and temparature diffustion coefficient (float) separated by spaces.")
        print("Running using standard values")
        print("64 10 100 3000 0.0 0.0 0.1")

        sim = Simulator(N=64, resolution=10, force = 100, source=3000, diff = 0.0, visc = 0.0, temp_diff=0.1)


    sim.Start()

    