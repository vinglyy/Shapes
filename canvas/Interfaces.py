"""
Zde najdete všechny interfacy
"""
from abc import ABC, abstractmethod


class ICopyable(ABC):
    @abstractmethod
    def copy(self):
        """Vrátí kopii instance"""


class IMovable(ABC):
    @abstractmethod
    def set_x(self, x: int):
        """
        Změna souřadnice x.
        """

    @abstractmethod
    def set_y(self, y: int):
        """Změna souřadnice y."""

    @abstractmethod
    def move_up(self, length=25):
        """
        Metoda pohne obrazcem nahoru.
        """

    @abstractmethod
    def move_down(self, length=25):
        """
        Metoda pohne obrazcem nahoru.
        """

    @abstractmethod
    def move_right(self, length=25) :
        """
        Metoda pohne obrazcem doprava.
        """

    @abstractmethod
    def move_left(self, length=25):
        """
        Metoda pohne obrazcem doleva.
        """

    @abstractmethod
    def set_position(self, x: int, y: int):
        """
        Metoda pohne obrazcem do určitého bodu.
        """