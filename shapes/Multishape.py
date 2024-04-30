from .Abstract_classes import IMovable, IRemovable
from .Shape import Shape
from abc import ABC
from .CanvasShapes import canvas


class Multishape(IMovable, IRemovable, ABC):
    """
    Instance třídy Multishape představuje komplexy geometrických
    tvarů které jsou určeny pro práci na virtuálním plátně při
    prvním seznámení s objekty. Tyto tvary mohou být složeny z
    několika jednodušších tvarů, které jsou instancemi rozhraní
    Shape. Pozice instance je definována jako pozice levého
    horního rohu obvodového obdélníku a její velikost je
    definována jako velikost tohoto obdélníku.
    Multishape je postupně složen z jednodušších tvarů, které
    musí být instancemi rozhraní Shape. Nejsou na ně kladeny
    žádné další požadavky. Během skládání se multishape
    automaticky opravuje své vnitřní informace o své poloze a
    velikosti takovým způsobem, aby pozice trvale směřovala do
    levého horního rohu obrázku. obvodového obdélníku a
    velikost odpovídá velikosti tohoto obdélníku.
    """

    def __init__(self, name: str = '', *parts):
        """
        Vytvoří multishape s daným názvem a případně složený z
        daných objektů, které jsou předány k vytvoření.
        objekty.
        :param name: Jméno multishapu
        :param parts: tvary, které chceme přidat
        """
        self._name = name
        self.parts = []
        self._x_pos = 0
        self._y_pos = 0
        self._height = 0
        self._width = 0
        self._first_shape = True
        self._creation_done = False
        self.add_shapes(*parts)

    def add_shapes(self, *args) -> None:
        """
        Přidá kopii daných tvarů do tohoto multishapu
         a vhodně upraví jeho vnitřní pozici a velikost.
        :param args: Tvar(y) které chceme přidat
        """
        if self._creation_done:
            raise Exception("Attempt to add a shape " +
                            "after finishing the creation " +
                            "of the mutlishape ")
        list_of_shapes = self._flatten_nested_list_or_tuple(args)
        for shape in list_of_shapes:
            if isinstance(shape, Shape):
                self.add_shape(shape)
            elif isinstance(shape, Multishape):
                for s in shape.parts:
                    self.add_shape(s.copy())
            else:
                raise Exception("Wrong arguments")

    @staticmethod
    def _flatten_nested_list_or_tuple(nested_list_or_tuple: tuple or list) -> list:
        """
        Metoda z vnořených listů nebo N-tic(tuple) tvarů vytvoří
        jednoduchý list tvarů.
        :param nested_list_or_tuple: list nebo N-tice
        :return: vrátí zploštělý list s tvary
        """
        flat_list = []
        for element in nested_list_or_tuple:
            if isinstance(element, (list, tuple)):
                flat_list.extend(Multishape._flatten_nested_list_or_tuple(element))
            elif isinstance(element, (Shape, Multishape)):
                flat_list.append(element)
            else:
                raise Exception("Unknown shape was attempted to be added to multishape")
        return flat_list

    def add_shape(self, shape: Shape) -> None:
        """
        Přidá zadaný tvar do multishapu a vhodně upraví jeho polohu a velikost.
        :param shape: tvar se má přidat do multishapu
        """
        if self._creation_done:
            raise Exception("Attempt to add a shape " +
                            "after finishing the creation " +
                            "of the mutlishape ")
        if self._first_shape:
            self._x_pos = shape.x
            self._y_pos = shape.y
            self._width = shape.width
            self._height = shape.height
            self._first_shape = False
        else:
            self._x_pos = min(self._x_pos, shape.x)
            self._y_pos = min(self._y_pos, shape.y)
            self._width = max(self._width, shape.width)
            self._height = max(self._height, shape.height)
        self.parts.append(shape)

    def creation_is_done(self) -> None:
        """
        Dokončí vytvoření multishape. Po zavolání této metody již
        nebude možné přidat další tvar do multishapu.
        """
        if len(self.parts) < 0:
            raise Exception("The multishape has to have at least one part")
        self._creation_done = True

    def _verify_done(self) -> None:
        """
        Ověřte, zda bylo vytvoření instance
        dokončeno pokud ne, vyhodí výjimku.
        """
        if self._creation_done:
            return
        raise Exception("Unfinished shape cannot run method")

    def set_size(self, width: int, height: int) -> None:
        """
        Nastaví nové rozměry instance.Upraví pozice a velikosti všech
        jejích částí tak, aby si multishape i přes novou velikost a
        pozici zachoval svůj vzhled. Velikost instance je
        definována jako velikost obvodového obdélníku. Nastavené
        rozměry musí být nezáporné, nulová hodnota je nahrazena
        jedničkou.
        :param width: Nová šířka instance
        :param height: Nová výška instance
        """
        self._verify_done()

        if width < 0 or height < 0:
            raise Exception("The dimensions may not be negativ: width=" + str(width) + ", height=" + str(height))

        scale_x = width / self._width if self._width != 0 else 1
        scale_y = height / self._height if self._height != 0 else 1
        for shape in self.parts:
            difference_x = shape.x - self._x_pos
            difference_y = shape.y - self._y_pos
            shape.set_size(scale_x * shape.width, scale_y * shape.height)
            shape.set_position(scale_x * difference_x + self._x_pos, scale_y * difference_y + self._y_pos)

        self._width = max(1, width)
        self._height = max(1, height)

    def set_position(self, x: int, y: int) -> None:
        """
        Přesunutí celého multishape na zadanou pozici. Všechny části
        se přesunou najednou jako jeden objekt. Poloha instance je
        definována jako poloha levého horního rohu obvodového
        obdélníku.
        :param x: Nově nastavená vodorovná souřadnice, levý
        okraj plátna má x=0, souřadnice se zvětšuje doprava.
        :param y: Nově nastavená svislá souřadnice, horní
        okraj plátna má y=0, souřadnice se zvyšuje směrem dolů.
        """
        # self.verify_done()
        dx = x - self._x_pos
        dy = y - self._y_pos
        for shape in self.parts:
            shape.set_position(dx + shape.x, dy + shape.y)
        self._x_pos = x
        self._y_pos = y

    def move_right(self, length=25):
        self.set_position(self._x_pos + length, self._y_pos)

    def move_left(self, length=25):
        self.set_position(self._x_pos - length, self._y_pos)

    def move_up(self, length=25):
        self.set_position(self._x_pos, self._y_pos - length)

    def move_down(self, length=25):
        self.set_position(self._x_pos, self._y_pos + length)

    def set_x(self, x: int):
        self.set_position(x, self._y_pos)

    def set_y(self, y: int):
        self.set_position(self._x_pos, y)

    def remove(self) -> None:
        """
        Metoda odstraní všechny tvary v multishapu z plátna
        """
        for part in self.parts:
            part.delete()

    def copy(self, new_name: str = None) -> 'Multishape':
        """
        Vytvoří kopii multishapu.
        :return: kopie multishapu
        """
        copy = Multishape(new_name if new_name else self._name + ' - copy')
        for part in self.parts:
            copy.add_shape(part.copy())
        return copy

    def __str__(self) -> str:
        """
        Vrátí informace o multishapu.
        :return: informace o multishapu
        """
        return "Multishape " + self._name + " with " + str(len(self.parts)) + " parts"

    def __repr__(self) -> str:
        """
        Vrátí informace o multishapu.
        :return: informace o multishapu
        """
        return self.__str__()

    def __len__(self) -> int:
        """
        Vrátí počet tvarů v multishapu.
        :return: počet tvarů v multishapu
        """
        return len(self.parts)

    def get_name(self) -> str:
        """
        Vrátí jméno multishapu.
        :return: name
        """
        return self._name

    def raise_above_shape(self, shape) -> None:
        """
        Zvedne obrazec nad jiný obrazec
        :param shape: pozice na kterou se má obrazec zvednout
        """
        print(reversed(self._get_parts_in_order()))
        for part in reversed(self._get_parts_in_order()):
            part.raise_above_shape(shape)

    def lower_below_shape(self, shape) -> None:
        """
        Snižuje obrazec pod jiný obrazec
        :param shape: pozice na kterou se má obrazec snížit
        """
        print(self._get_parts_in_order())
        for part in self._get_parts_in_order():
            part.lower_below_shape(shape)

    def _get_parts_in_order(self) -> list:
        """
        Vrátí list tvarů v multishapu v pořadí, v jakém jsou v display listu v kanvasu.
        :return:
        """
        list_all = canvas.find_all()
        dict_in_multishape = {}
        list_parts_in_order = []
        for s in self.parts:
            dict_in_multishape.update({s.canvas_id: s})
        for i in list_all:
            if i in dict_in_multishape.keys():
                list_parts_in_order.append(dict_in_multishape.get(i))
        return list_parts_in_order

    def get_highest_shape(self) -> Shape | None:
        """
        Vrátí nejvyšší tvar v multishapu.
        :return: nejvyšší tvar
        """
        list_all = canvas.find_all()
        dict_in_multishape = {}
        for s in self.parts:
            dict_in_multishape.update({s.canvas_id: s})

        for i in reversed(list_all):
            if i in dict_in_multishape.keys():
                return dict_in_multishape.get(i)
        return None

    def get_lowest_shape(self) -> Shape | None:
        """
        Vrátí nejnižší tvar v multishapu.
        :return: nejnižší tvar
        """
        list_all = canvas.find_all()
        dict_in_multishape = {}
        for s in self.parts:
            dict_in_multishape.update({s.canvas_id: s})

        for i in list_all:
            if i in dict_in_multishape.keys():
                return dict_in_multishape.get(i)
        return None
