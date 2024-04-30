from abc import ABC
from .Abstract_classes import Resizable, ID, Paintable, ICopyable, IRemovable
from .NamedColor import YELLOW
from .CanvasShapes import canvas


class Shape(Resizable, ID, Paintable, ICopyable, IRemovable, ABC):
    """
    Rodičovská implementace obrazců, slouží k tomu aby
    jsme se nemusely psát metody pro některé obrazce
    několikrát.
    Také jsou zde implementována abstraktní třída, aby
    nešlo vytvořit Shape instanci.
    """

    def __init__(self, x, y, width, height, color=YELLOW):
        """
        Initializační dunder metoda pro třídu Shape.
        x a y jsou v pravém horním rohu.
        Také počítá id, každý obrazec má svoje číslo
        :param x: osa x
        :param y: osa y, nahoru je méně, dolu je více
        :param width: šířka obrazce
        :param height: výška obrazce
        :param color: barva obrazce, je třeba použít metody NamedColor
        """
        ID.__init__(self)
        canvas.all_shapes.append(self)
        Resizable.__init__(self, x, y, width, height)

        self.color = color
        Paintable.__init__(self)

    def rub_out(self) -> None:
        """
        Dočasně přebarví tvar na barvu pozadí.
        """
        canvas.itemconfig(self.__repr__(), fill=canvas.canvas_color.tkn)
        canvas.update_shapes()

    def change_shape_color(self, color=None) -> None:
        """
        Změní barvu obrazce na tu která je uložená ve třídě,
        pokud vsak požit parametr s platnou COLOR tak na
        tuto barvu.
        """
        if color is not None:
            self.color = color
        canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
        canvas.update_shapes()

    def _count_corners(self) -> None:
        """
        Přepočítá souřadnice
        """
        self.corner_1 = (self.x, self.y)
        self.corner_2 = (self.x + self.width, self.y + self.height)

    def get_coord(self) -> list:
        """
        Z 2 corners vytvoří list
        :return: vrací souřadnice v jedné proměnné
        """
        coord = [item for sublist in [self.corner_1, self.corner_2]
                 for item in sublist]
        return coord

    def to_string(self) -> str:
        """
        Metoda vrátí info o obrazci
        :return: String s informavemi o obrazci
        """
        return self.__repr__() + "[x =" + str(self.x) + \
            " y =" + str(self.y) + " height =" + str(self.height) \
            + " width =" + str(self.width) + " color = " + \
            str(self.color._name) + "]"  # noqa

    def remove(self):
        """
        Odstraní tvar z plátna.
        """
        self._is_painted_on_canvas = False
        canvas.delete(self.id)

    def raise_above_shape(self, shape) -> None:
        """
        Zvedne obrazec nad jiný obrazec
        :param shape: pozice na kterou se má obrazec zvednout
        """
        if isinstance(shape, Shape):
            canvas.tag_raise(self.__repr__(), shape.__repr__())
        else:
            canvas.tag_raise(self.__repr__(), shape.get_highest_shape().__repr__())
        canvas.update_shapes()

    def lower_below_shape(self, shape) -> None:
        """
        Snižuje obrazec pod jiný obrazec
        :param shape: pozice na kterou se má obrazec snížit
        """
        if isinstance(shape, Shape):
            canvas.tag_lower(self.__repr__(), shape.__repr__())
        else:
            canvas.tag_lower(self.__repr__(), shape.get_lowest_shape().__repr__())
        canvas.update_shapes()

    def raise_to_top(self) -> None:
        """
        Zvedne obrazec na vrchol
        """
        canvas.tag_raise(self.__repr__())
        canvas.update_shapes()

    def lower_to_bottom(self) -> None:
        """
        Snižuje obrazec na dno
        """
        canvas.tag_lower(self.__repr__())
        canvas.update_shapes()
