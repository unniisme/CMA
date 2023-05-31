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

        self.get_display_matrix = self.fluid.get_density
        self.thermals = False

    def DrawSquare(self, gridStart : tuple, length : int, offset : int, colour : tuple = (0,0,255)):
        # Function to draw a single grid cell
        rect = pygame.Rect(gridStart[0] + offset, gridStart[1] + offset, length - 2*offset, length - 2*offset)
        pygame.draw.rect(self.screen, colour, rect)

    def density_color(self, i,j):
        col = round(self.get_display_matrix()[i,j]*255/10)
        col = max(0, min(255,col))
        if not self.thermals:
            return (col, col, col)
        else:
            # Thermal red
            return (col, 10, 10)

    def DrawGrid(self, in_offset : int = 0):

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                # Draw each square of grid
                self.DrawSquare((i*self.gridSize,j*self.gridSize), self.gridSize, in_offset, self.density_color(i,j))
    
    def Vector2ToGridCell(self, vector2):
        """
        Given a vector2 return the corresponding indices of the grid cell
        that contains it.
        """
        x = int(vector2[0] / self.gridSize)
        y = int(vector2[1] / self.gridSize)
        return (x, y)

    def Start(self, showInstructions=True):

        if showInstructions:
            print()
            print("Navier stokes simulation written by https://github.com/unniisme")
            print("Reference: https://www.dgp.toronto.edu/public_user/stam/reality/Research/pdf/GDC03.pdf")
            print("Click to add bits of fluid")
            print("Right Click and drag to add a current")

        pygame.init()

        # Text initialisaton
        coordinates = "(0,0)"
        text = pygame.font.Font('freesansbold.ttf', 10).render(coordinates, True, (255,255,255))
        textRect = text.get_rect()
        textRect.topleft = (0,0)

        while True:

            self.fluid.solver.density_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.u_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.v_prev = np.zeros(self.fluid.solver.dimensions)

            for e in pygame.event.get():
                # If user clicks close button, exit the loop
                if e.type == pygame.QUIT:
                    return 0
                # Check if a key is pressed down
                if e.type == pygame.KEYDOWN:
                    # if 'r' is pressed, toggle between thermal and density display modes
                    if e.key == pygame.K_r:
                        self.thermals = not self.thermals
                        if self.thermals:
                            self.get_display_matrix = self.fluid.get_temp
                        else:
                            self.get_display_matrix = self.fluid.get_density

            # Get the current mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Get the relative movement of the mouse since the last call to get_rel()
            mouse_delta = pygame.mouse.get_rel()

            # Convert the mouse position to a grid cell coordinate
            coordinates = str(self.Vector2ToGridCell(mouse_pos))

            # Check if the left mouse button is pressed down
            if pygame.mouse.get_pressed()[0]:
                # Add density and heat to the grid at the current mouse position
                self.fluid.add_density(*self.Vector2ToGridCell(mouse_pos), self.source)
                self.fluid.add_heat(*self.Vector2ToGridCell(mouse_pos), self.source)

            # Check if the right mouse button is pressed down
            if pygame.mouse.get_pressed()[2]:
                # Add velocity to the grid in the direction of the mouse movement at the current position
                mouse_force = (mouse_delta[0]*self.force, mouse_delta[1]*self.force)
                self.fluid.add_velocity(*self.Vector2ToGridCell(mouse_pos), *mouse_force)

            # Update the fluid grid
            self.fluid.update()

            # Redraw the grid and display the coordinate of the current mouse position
            self.screen.fill((255,255,255))
            self.DrawGrid()
            text = pygame.font.Font('freesansbold.ttf', 10).render(coordinates, True, (255,255,255))
            textRect = text.get_rect()
            textRect.topleft = (0,0)
            self.screen.blit(text, textRect)
            pygame.display.flip()

            # Wait until next frame is due and exit the loop if pygame.QUIT event has been sent
            self.clock.tick(self.fps)


    