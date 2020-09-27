import pygame
import sys
import random


class Node:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._neighbours = list()
        self._connected = list()
        self._visited = False

    def add_neighbour(self, node):
        self._neighbours.append(node)

    def connect(self, node):
        self._connected.append(node)
        self.del_node(node)

    def del_node(self, node):
        for index, neighbour in enumerate(self._neighbours):
            if neighbour == node:
                del self._neighbours[index]
                return

    def connect_next(self):
        self._visited = True
        while self._neighbours:
            neighbour = random.choice(self._neighbours)
            if not neighbour._visited:
                self.connect(neighbour)
                neighbour.connect(self)
                neighbour.connect_next()
            else:
                self.del_node(neighbour)


    @property
    def position(self):
        return self._x, self._y

    @property
    def north(self):
        for neighbour in self._connected:
            if self.position[1] - 1 == neighbour.position[1]:
                return True
        return False

    @property
    def east(self):
        for neighbour in self._connected:
            if self.position[0] + 1 == neighbour.position[0]:
                return True
        return False

    @property
    def south(self):
        for neighbour in self._connected:
            if self.position[1] + 1 == neighbour.position[1]:
                return True
        return False

    @property
    def west(self):
        for neighbour in self._connected:
            if self.position[0] - 1 == neighbour.position[0]:
                return True
        return False


def draw_grid(surface, size, nodes, cells, padding=0):
    single_width = int((size[0] - 2 * padding) / cells[0])
    single_height = int((size[1] - 2 * padding) / cells[1])

    for x in range(0, cells[0]):
        for y in range(0, cells[1]):
            x_pos = padding + x * single_width
            y_pos = padding + y * single_height
            if not nodes[x][y].north:
                pygame.draw.line(surface, (255, 255, 255), (x_pos, y_pos), (x_pos + single_width, y_pos))
            if not nodes[x][y].east:
                pygame.draw.line(surface, (255, 255, 255), (x_pos + single_width, y_pos),
                                 (x_pos + single_width, y_pos + single_height))
            if not nodes[x][y].south:
                pygame.draw.line(surface, (255, 255, 255), (x_pos, y_pos + single_height),
                                 (x_pos + single_width, y_pos + single_height))
            if not nodes[x][y].west:
                pygame.draw.line(surface, (255, 255, 255), (x_pos, y_pos),
                                 (x_pos, y_pos + single_height))


class GameEngine:
    def __init__(self, size):
        pygame.init()
        # speed = [2, 2]
        # black = 0, 0, 0
        self._number = [0, 0]
        self._finished = False
        self._cells = (150, 110)
        self._size = size
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._size)
        self._surface = pygame.Surface(self._screen.get_size())
        self._surface = self._surface.convert()
        self._nodes = list()
        for x in range(0, self._cells[0]):
            self._nodes.append(list())
            for y in range(0, self._cells[1]):
                self._nodes[x].append(Node(x, y))
        for x in range(0, self._cells[0]):
            for y in range(0, self._cells[1]):
                if x != 0:
                    self._nodes[x][y].add_neighbour(self._nodes[x-1][y])
                if x != self._cells[0]-1:
                    self._nodes[x][y].add_neighbour(self._nodes[x+1][y])
                if y != 0:
                    self._nodes[x][y].add_neighbour(self._nodes[x][y-1])
                if y != self._cells[1]-1:
                    self._nodes[x][y].add_neighbour(self._nodes[x][y+1])
        # self._single_size = draw_grid(self._surface, self._size, cells=self._nodes)
        draw_grid(self._surface, self._size, nodes=self._nodes, cells=self._cells)
        # self._snake = Snake(self._single_size, self._cells)
        # self._snack = Snack(self._single_size, self._cells)


    def update(self):
        self._nodes[0][0].connect_next()

        # self._snake.move()
        # if self._snake.colides():
        #     self._snake = Snake(self._single_size, self._cells)
        # self._snake.eat(self._snack)
        # self._snake.draw(self._surface)
        # self._snack.draw(self._surface)

    def run(self):
        while True:
            self._clock.tick(10)
            self._surface.fill((0, 0, 0))
            draw_grid(self._surface, self._size, self._nodes, self._cells, padding=20)
            self.handle_keys()
            self.update()
            pygame.display.update()
            self._screen.blit(self._surface, (0, 0))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)


def main():
    sys.setrecursionlimit(10 ** 6)
    GameEngine((800, 600)).run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
