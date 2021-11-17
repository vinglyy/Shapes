"""
Zde najdete všechjny abstraktní třídy
"""


from .Interfaces import *


class ID(ABC):
    _counter = 0

    def __init__(self):
        ID._counter += 1
        self.id = str(ID._counter)

    def __repr__(self) -> str:
        """
        Dunderová metota
        :return: str s jménem řídy a id třídy
        """
        return self.__class__.__name__ + self.id


class Coord(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Movable(Coord, IMovable, ABC):
    def set_x(self, x: int) -> None:
        """
        Změna coordinát
        :param x:
        """
        self.x = x
        self._count_corners()
        self.paint()

    def set_y(self, y: int) -> None:
        self.y = y
        self._count_corners()
        self.paint()

    def move_up(self, length=25) -> None:
        """
        Metoda pohne obrazcem nahoru
        :param length: jak dlouhý má být krok
        """
        self.y -= length
        self._count_corners()
        self.paint()

    def move_down(self, length=25) -> None:
        """
        Metoda pohne obrazcem nahoru
        :param length: jak dlouhý má být krok
        """
        self.y += length
        self._count_corners()
        self.paint()

    def move_right(self, length=25) -> None:
        """
        Metoda pohne obrazcem doprava
        :param length: jak dlouhý má být krok
        """
        self.x += length
        self._count_corners()
        self.paint()

    def move_left(self, length=25) -> None:
        """
        Metoda pohne obrazcem doleva
        :param length: jak dlouhý má být krok
        """
        self.x -= length
        self._count_corners()
        self.paint()

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self._count_corners()
        self.paint()


class Resizable(Movable, Coord, ABC):
    def __init__(self, x, y, width, height):
        Coord.__init__(self,x,y)
        Movable.__init__(self,x,y)

        self.height = height
        self.width = width

        self.corner_1 = (x, y)
        self.corner_2 = (x + width, y + height)

    def set_width(self, width: int) -> None:
        self.width = width
        self._count_corners()
        self.paint()

    def set_height(self, height: int) -> None:
        self.height = height
        self._count_corners()
        self.paint()

    def set_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._count_corners()
        self.paint()


class Paintable(ABC):
    def __init__(self):
        self._is_painted_on_canvas = False
        self.paint()

    @abstractmethod
    def paint(self):
        pass
