import pygame
from NavierStokes import Simulation, WaterSimulation
import numpy as np
import sys

class Simulator:

    def __init__ (self, N = 20, resolution = 30, force = 5, source = 1000, diff = 0.0, visc = 0.0, temp_diff = 0.1, isWaterSim=False):
        self.fps = 60
        self.screenSize = [N*resolution]*2
        self.screen = pygame.display.set_mode(self.screenSize)
        self.clock = pygame.time.Clock()
        self.running = True

        self.force = force
        self.source = source

        self.gridSize = resolution
        self.dimensions = (N, N)

        if isWaterSim:
            self.fluid = WaterSimulation(N-2, diff, visc, temp_diff, 0.1)
        else:
            self.fluid = Simulation(N-2, diff, visc, temp_diff, 0.01)

    def DrawSquare(self, gridStart : tuple, length : int, offset : int, colour : tuple = (0,0,255)):
        rect = pygame.Rect(gridStart[0] + offset, gridStart[1] + offset, length - 2*offset, length - 2*offset)
        pygame.draw.rect(self.screen, colour, rect)

    def density_color(self, i,j):
        col = round(self.fluid.get_density()[i,j]*255/10)
        col = max(0, min(255,col))
        return (col, col, col)

    def DrawGrid(self, in_offset : int = 0):

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                self.DrawSquare((i*self.gridSize,j*self.gridSize), self.gridSize, in_offset, self.density_color(i,j))
    
    def Vector2ToGridCell(self, vector2):
        """
        Given a vector2 return the corresponding indices of the grid cell
        that contains it.
        """
        x = int(vector2[0] / self.gridSize)
        y = int(vector2[1] / self.gridSize)
        return (x, y)

    def Start(self):

        pygame.init()

        coordinates = "(0,0)"
        text = pygame.font.Font('freesansbold.ttf', 10).render(coordinates, True, (255,255,255))
        textRect = text.get_rect()
        textRect.topleft = (0,0)

        while True:

            self.fluid.solver.density_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.u_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.v_prev = np.zeros(self.fluid.solver.dimensions)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return 0

            mouse_pos = pygame.mouse.get_pos()
            mouse_delta = pygame.mouse.get_rel()

            coordinates = str(self.Vector2ToGridCell(mouse_pos))

            if pygame.mouse.get_pressed()[0]:
                self.fluid.add_density(*self.Vector2ToGridCell(mouse_pos), self.source)
                # self.fluid.add_density(self.Vector2ToGridCell(mouse_pos), self.source)

            if pygame.mouse.get_pressed()[2]:
                # self.fluid.solver.u_prev[self.Vector2ToGridCell(mouse_pos)] = self.force * mouse_delta[0]
                # self.fluid.solver.v_prev[self.Vector2ToGridCell(mouse_pos)] = self.force *mouse_delta[1]
                mouse_force = (mouse_delta[0]*self.force, mouse_delta[1]*self.force)
                self.fluid.add_velocity(*self.Vector2ToGridCell(mouse_pos), *mouse_force)

            self.fluid.update()

            self.screen.fill((255,255,255))
            self.DrawGrid()

            text = pygame.font.Font('freesansbold.ttf', 10).render(coordinates, True, (255,255,255))
            textRect = text.get_rect()
            textRect.topleft = (0,0)
            self.screen.blit(text, textRect)

            pygame.display.flip()
            self.clock.tick(self.fps)

    