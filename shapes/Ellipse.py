from .Shape import Shape
from .CanvasShapes import canvas, canvas_step
from .NamedColor import BLUE


class Ellipse(Shape):
    """
    Instance třídy Ellipse představují elipsy
    které jsou určeny pro práci na virtuálním plátně
    při prvním seznámení s objekty.
    Jsou definovány svou polohou, velikostí a barvou.
    Poloha instance je definována jako pozice
    levého horního rohu obvodového obdélníku.
    a její velikost je definována jako velikost
    tohoto obdélníku.
    """

    def __init__(self, x=0, y=0, width=2 * canvas_step, height=canvas_step, color=BLUE):
        """
        Vytvoří novou instanci Ellipse
        :param x: Vodorovná souřadnice, levý okraj plátna má x=0,
        souřadnice se zvětšuje směrem doprava.
        defaultně 0
        :param y: Svislá souřadnice, horní okraj plátna má y=0,
        souřadnice se zvyšuje směrem dolů.
        základně 0
        :param width: šířka instance
        základně 50(2 * canvas_step)
        :param height: výška instance
        základně 25 canvas_step
        :param color: barva instance
        základně BLUE
        """
        super().__init__(x, y, width, height, color)

    def paint(self) -> None:
        """
        Tato metoda zavolá plátno a pokud tvar ještě nebyl
        vytvořen tak na něm vytvoří nový, pokud již byl tak
        aktualizuje tvar na plátně podle atributů x,y,width,
        height a color.
        """
        if not self._is_painted_on_canvas:
            self.canvas_id = canvas.create_oval(self.get_coord(), tag=self.__repr__(),
                                                fill=self.color.tkn, width=0, outline="")
            self._is_painted_on_canvas = True
            canvas.update_shapes()
        else:
            canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.update_shapes()

    def copy(self) -> Shape:
        return Ellipse(self.x, self.y, self.width, self.height, self.color)
