import shapes.Direction8 as directions

from .Shape import Shape
from .NamedColor import *
from .CanvasShapes import canvas, canvas_step


class Triangle(Shape):
    """
    Instance třídy code Triangle představuje trojúhelníky
    které jsou určeny pro práci na virtuálním plátně
    při prvním seznámení s objekty.
    Jsou definovány svou polohou, velikostí, barvou a směrem.
    do kterého je natočen hlavní vrchol.
    Poloha instance je definována jako pozice
    levého horního rohu obvodového obdélníku.
    a její velikost je definována jako velikost tohoto obdélníku.
    Směr trojúhelníku je směr
    do kterého je natočen hlavní vrchol trojúhelníku.
    """

    def __init__(self, x=0, y=0, width=2 * canvas_step,
                 height=canvas_step, color=YELLOW, dir8=directions.NORTH):
        """
        Vytvoří novou instanci Triangle
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
        základně YELLOW
        :param dir8: Směr, kterým je natočen hlavní vrchol.
        základně NORTH
        """
        self.dir8 = dir8
        super().__init__(x, y, width, height, color)

    def paint(self) -> None:
        """
        Metoda paint vytvoří tvar na plátně, pokud není vytvořen.
        Pokud je pouze aktualizuje stav tvaru na plátně podle
        atributů třídy.
        """
        if not self._is_painted_on_canvas:
            self.canvas_id = canvas.create_polygon(self.get_coord(), tag=self.__repr__(),
                                  fill=self.color.tkn, width=0)
            self._is_painted_on_canvas = True
            canvas.update_shapes()
        else:
            canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.update_shapes()

    def get_coord(self) -> list:
        """
        Přepočítá body tak aby jsme dostaly výstup, který můžeme
        použít na plátně.
        """
        coord = [int, int, int, int, int, int]
        match self.dir8:
            case directions.NORTH:
                coord[0] = (self.corner_1[0] + self.corner_2[0]) / 2
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case directions.NORTH_EAST:
                coord[0] = self.corner_2[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_1[1]
            case directions.EAST:
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = (self.corner_1[1] + self.corner_2[1]) / 2
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case directions.SOUTH_EAST:
                coord[0] = self.corner_2[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case directions.SOUTH:
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_1[1]
                coord[4] = (self.corner_1[0] + self.corner_2[0]) / 2
                coord[5] = self.corner_2[1]
            case directions.SOUTH_WEST:
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case directions.WEST:
                coord[0] = self.corner_2[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = (self.corner_1[1] + self.corner_2[1]) / 2
            case directions.NORTH_WEST:
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_1[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
        return coord

    def set_direction(self, direction):
        """
        Tato metoda změní směr trojúhelníku.
        :param direction: směr
        """
        self.dir8 = direction
        self.get_coord()
        self.paint()

    def copy(self) -> Shape:
        return Triangle(self.x, self.y, self.width,
                        self.height, self.color, self.dir8)
