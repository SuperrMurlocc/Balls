import random
import pygame
import consts as c


def distance(p1: (int, int), p2: (int, int)) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** .5


class Dot:
    """
    Class used to create a dot object.
    """

    def __init__(self, name: str, r_size: int, color: (int, int, int), size_change: int = 0, max_move_speed: int = 5, pos: (int, int) = None):
        """
        Initializes dot object.

        :param name: Name of dot.
        :param r_size: Radius size of dot.
        :param color: Color of dot.
        :param size_change: The amount by which our dot size is changed.
        :param pos: Position of dot.
        """
        self.name = name
        self.r_size = r_size
        self.color = color
        self.size_change = size_change
        if pos:
            self.pos_x = pos[0]
            self.pos_y = pos[1]
        else:
            self.pos_x = random.randint(r_size, c.SCREEN_WIDTH - r_size)
            self.pos_y = random.randint(r_size, c.SCREEN_HEIGHT - r_size)

        self.max_move_speed = max_move_speed

        self.move = random.randint(-max_move_speed, max_move_speed)
        self.move_direction = random.randint(0, 1)

    def disp(self, screen) -> None:
        """
        Displays dot on screen.

        :return: None
        """
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.r_size)

    def collision(self, pos_x, pos_y) -> bool:
        """
        Detect collison.

        :return: True/False.
        """
        if distance((self.pos_x, self.pos_y), (pos_x, pos_y)) <= c.CIRCLE_R_SIZE + self.r_size:
            return True
        else:
            return False

    def determine_move(self):
        self.move = random.randint(-self.max_move_speed, self.max_move_speed) * c.MULT
        self.move_direction = random.randint(0, 1)

    def move_pos(self):
        if self.move_direction:
            self.pos_x += self.move

            if self.pos_x < self.r_size:
                self.pos_x = self.r_size
            if self.pos_x > c.SCREEN_WIDTH - self.r_size:
                self.pos_x = c.SCREEN_WIDTH - self.r_size
        else:
            self.pos_y += self.move

            if self.pos_y < self.r_size:
                self.pos_y = self.r_size
            if self.pos_y > c.SCREEN_HEIGHT - self.r_size:
                self.pos_y = c.SCREEN_HEIGHT - self.r_size