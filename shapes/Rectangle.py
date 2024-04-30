from .Shape import Shape
from .CanvasShapes import canvas, canvas_step
from .NamedColor import RED

class Rectangle(Shape):
    """
    Instance třídy  Rectangle představují obdélníky
    které jsou určeny pro práci na virtuálním plátně
    při prvním seznámení s objekty.
    Jsou definovány svou polohou, velikostí a barvou.
    Pozice instance je definována jako pozice
    jeho levého horního rohu.
    """

    def __init__(self, x=0, y=0, width=2 * canvas_step, height=canvas_step, color=RED):
        """
        Vytvoří novou instanci Rectangle
        :param x: Vodorovná souřadnice, levý okraj plátna má x=0,
        souřadnice se zvětšuje směrem doprava.
        základně 0
        :param y: Svislá souřadnice, horní okraj plátna má y=0,
        souřadnice se zvyšuje směrem dolů.
        základně 0
        :param width: šířka instance
        základně 50(2 * canvas_step)
        :param height: výška instance
        základně 25 canvas_step
        :param color: barva instance
        základně RED
        """
        super().__init__(x, y, width, height, color)

    def paint(self) -> None:
        """
        Metoda paint vytvoří tvar na plátně, pokud není vytvořen.
        Pokud je pouze aktualizuje stav tvaru na plátně podle
        atributů třídy.
        """
        if not self._is_painted_on_canvas:
            self.canvas_id = canvas.create_rectangle(self.get_coord(), tag=self.__repr__(), fill=self.color.tkn, width=0)
            self._is_painted_on_canvas = True
            canvas.update_shapes()
        else:
            canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.update_shapes()

    def copy(self) -> Shape:
        return Rectangle(self.x, self.y, self.width, self.height, self.color)
