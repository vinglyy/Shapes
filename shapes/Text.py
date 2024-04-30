from .Abstract_classes import Movable, ICopyable, IRemovable, ID, Paintable
from .CanvasShapes import canvas


class Text(Movable, ID, Paintable, ICopyable, IRemovable):
    """
    Instance třídy Text. Vytvoří normální text na plátně.
    Text je možné:
        posouvat,
        změnit text
        okopírovat
        odstranit z plátna
    """

    def __init__(self, x=0, y=0, text="text"):
        """
        Vytvoří instanci třídy Text.
        :param x: x souřadnice, základně 0
        :param y: y souřadnice, základně 0
        :param text: text který bude vypsán, základně "text"
        """
        ID.__init__(self)
        Movable.__init__(self, x, y)
        self.text = text
        Paintable.__init__(self)
        self.paint()

    def paint(self) -> None:
        """
        Metoda paint vytvoří tvar na plátně, pokud není vytvořen.
        Pokud je pouze aktualizuje stav tvaru na plátně podle
        atributů třídy.
        """
        if not self._is_painted_on_canvas:
            self.canvas_id = canvas.create_text(self.x, self.y, text=self.text, tag=self.__repr__())
            self._is_painted_on_canvas = True
        else:
            canvas.itemconfig(self.__repr__())
            canvas.coords(self.__repr__(), self.x, self.y)
            canvas.update_shapes()

    def copy(self):
        """
        Metoda vrátí kopii tvaru.
        :return: vracená kopie tvaru
        """
        return Text(self.x, self.y, self.text)

    def set_text(self, text):
        """
        Změní text, který je zobrazen.
        :param text: text
        """
        self.text = text
        self.paint()

    def remove(self):
        """
        Odstraní text z plátna. Nezničí ale objekt, takže je ho
        možné znovu zobrazit na plátně pomocí metody paint.
        """
        self._is_painted_on_canvas = False
        canvas.delete(self.id)
