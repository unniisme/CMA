import pygame
from NavierStokes import SmokeSimulation

class Simulator:

    def __init__ (self, N = 20, resolution = 30):
        self.fps = 60
        screenSize = [N*resolution]*2
        self.screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()
        self.running = True

        self.force = 500
        self.source = 1000

        self.gridSize = resolution
        self.dimensions = (N, N)

        self.fluid = SmokeSimulation(N, 0.01, 0.01, 0.1)

    def DrawSquare(self, gridStart : tuple, length : int, offset : int, colour : tuple = (0,0,255)):
        rect = pygame.Rect(gridStart[0] + offset, gridStart[1] + offset, length - 2*offset, length - 2*offset)
        pygame.draw.rect(self.screen, colour, rect)

    def DrawGrid(self, in_offset : int = 1):

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                col = round(255 - self.fluid.get_density()[i,j]*255/500)
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
            mouse_delta = pygame.mouse.get_rel()

            if pygame.mouse.get_pressed()[0]:
                self.fluid.add_density(*self.Vector2ToGridCell(mouse_pos), self.source)

            self.fluid.add_velocity(*self.Vector2ToGridCell(mouse_pos), *self.Vector2ToGridCell(mouse_delta*self.force))

            self.fluid.update()

            self.screen.fill((255,255,255))

            self.DrawGrid()

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    sim = Simulator()

    # sim.fluid.D[5,5] = 1000
    # sim.fluid.D_prev[5,5] = 1000


    sim.Start()
    