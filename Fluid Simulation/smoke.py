from simulator import Simulator
import sys

if __name__ == '__main__':

    if len(sys.argv) == 7:
        N = int(sys.argv[1])
        resolution = int(sys.argv[2])
        force = int(sys.argv[3])
        source = int(sys.argv[4])
        diff = float(sys.argv[5])
        visc = float(sys.argv[6])

        sim = Simulator(N, resolution, force, source, diff, visc)


    else:
        print("Invalid input format. Please enter 6 arguments: N (int), resolution (int), force (int), source (int), diff (float), and visc (float) separated by spaces.")
        print("Running using standard values")
        print("64 20 70 1000 0.0 0.0")

        sim = Simulator(N=64, resolution=20, force = 70, source=1000, diff = 0.0, visc = 0.0)


    sim.Start()

    