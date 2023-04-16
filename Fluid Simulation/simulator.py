import pygame
from NavierStokes import NS, NS_sim
import numpy as np

class Simulator:

    def __init__ (self, screenSize = [800, 600], gridSize = 10):
        self.fps = 60
        self.screen = pygame.display.set_mode(screenSize)
        self.screenSize = screenSize
        self.gridSize = gridSize
        self.clock = pygame.time.Clock()
        self.running = True

        self.dimensions = (screenSize[0]//gridSize, screenSize[1]//gridSize)

        self.fluid = NS_sim(self.dimensions)

    def DrawSquare(self, gridStart : tuple, length : int, offset : int, colour : tuple = (0,0,255)):
        rect = pygame.Rect(gridStart[0] + offset, gridStart[1] + offset, length - 2*offset, length - 2*offset)
        pygame.draw.rect(self.screen, colour, rect)

    def DrawGrid(self, in_offset : int = 1):

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                col = round(255 - self.fluid.D[i,j]*255/500)
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
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return 0

            mouse_pos = pygame.mouse.get_pos()


            self.screen.fill((255,255,255))

            self.fluid.D[self.Vector2ToGridCell(mouse_pos)] += (1/self.fps) * 100000
            self.fluid.D_prev[self.Vector2ToGridCell(mouse_pos)] += (1/self.fps) * 100000

            # for i in range(self.fluid.dimensions[0]):
            #     for j in range(self.fluid.dimensions[1]):
            #         pygame.draw.line(self.screen, (0,0,0), (se), end_pos)

            self.fluid.update(1/self.fps)
            # self.fluid.diffuse(self.fluid.D, self.fluid.D_prev, self.fluid.diff_coeff, 1/self.fps)

            print(np.argmax(self.fluid.D), np.max(self.fluid.D))

            self.DrawGrid()

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    sim = Simulator(gridSize = 50)

    # sim.fluid.D[5,5] = 1000
    # sim.fluid.D_prev[5,5] = 1000


    sim.Start()
    