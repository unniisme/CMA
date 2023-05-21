import pygame
from NavierStokes import SmokeSimulation
import numpy as np
import sys

class Simulator:

    def __init__ (self, N = 20, resolution = 30, force = 5, source = 1000, diff = 0.0, visc = 0.0):
        self.fps = 60
        screenSize = [N*resolution]*2
        self.screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()
        self.running = True

        self.force = 5
        self.source = 1000
        diff = 0.0
        visc = 0.0

        self.gridSize = resolution
        self.dimensions = (N, N)

        self.fluid = SmokeSimulation(N-2, diff, visc, 0.1)

    def DrawSquare(self, gridStart : tuple, length : int, offset : int, colour : tuple = (0,0,255)):
        rect = pygame.Rect(gridStart[0] + offset, gridStart[1] + offset, length - 2*offset, length - 2*offset)
        pygame.draw.rect(self.screen, colour, rect)

    def DrawGrid(self, in_offset : int = 0):

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                col = round(self.fluid.get_density()[i,j]*255/10)
                col = max(0, min(255,col))
                self.DrawSquare((i*self.gridSize,j*self.gridSize), self.gridSize, in_offset, (col,col,col))
    
    def Vector2ToGridCell(self, vector2):
        """
        Given a vector2 return the corresponding indices of the grid cell
        that contains it.
        """
        x = int(vector2[0] / self.gridSize)
        y = int(vector2[1] / self.gridSize)
        return (x, y)

    def Start(self):

        while True:

            self.fluid.solver.density_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.u_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.v_prev = np.zeros(self.fluid.solver.dimensions)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return 0

            mouse_pos = pygame.mouse.get_pos()
            mouse_delta = pygame.mouse.get_rel()

            if pygame.mouse.get_pressed()[0]:
                # self.fluid.add_density(*self.Vector2ToGridCell(mouse_pos), self.source)
                self.fluid.solver.density_prev[self.Vector2ToGridCell(mouse_pos)] = self.source

            if pygame.mouse.get_pressed()[2]:
                self.fluid.solver.u_prev[self.Vector2ToGridCell(mouse_pos)] = self.force * mouse_delta[0]
                self.fluid.solver.v_prev[self.Vector2ToGridCell(mouse_pos)] = self.force *mouse_delta[1]
                # mouse_force = (mouse_delta[0]*self.force, mouse_delta[1]*self.force)
                # self.fluid.add_velocity(*self.Vector2ToGridCell(mouse_pos), *mouse_force)

            self.fluid.update()

            self.screen.fill((255,255,255))

            self.DrawGrid()

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        sim = Simulator(N=64, resolution=20, force = 70, source=1000, diff = 0.0, visc = 0.0)

    else:
        N = int(sys.argv[1])
        resolution = int(sys.argv[2])
        force = int(sys.argv[3])
        source = int(sys.argv[4])
        diff = float(sys.argv[5])
        visc = float(sys.argv[6])

        sim = Simulator(N, resolution, force, source, diff, visc)


    # sim.fluid.D[5,5] = 1000
    # sim.fluid.D_prev[5,5] = 1000


    sim.Start()
    