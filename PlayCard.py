from dataclasses import dataclass
from enum import Enum, unique


@unique
class CardFamily(Enum):
    KREUZ = 4
    PIK = 3
    HERZ = 2
    KARO = 1


@unique
class CardFace(Enum):
    AS = 11
    ZEHN = 10
    KOENIG = 4
    DAME = 3
    BUBE = 2
 
    
@dataclass(frozen=True)
class PLayCard:
    _family: CardFamily
    _face: CardFace
    _db_id: int
    image_path: str = 'E:/User/Projects/Python Doko/Images/'
    
    @property
    def family(self):
        return self._family

    @property
    def face(self):
        return self._face

    @property
    def db_id(self):
        return self._db_id

    @property
    def image(self):
        return f'{self.image_path}{self._family.name.capitalize()}' + \
                f'_{self.face.name.capitalize()}.gif'

    def __post_init__(self):
        if not isinstance(self._family, CardFamily):
            raise ValueError('family muss Kartenfamile sein (KREUZ, PIK, ... ) ')
        if not isinstance(self.face, CardFace):
            raise ValueError('face muss Kartengesicht sein (AS, ZEHN, ... ) ')
        if not isinstance(self.db_id, int):
            raise ValueError('db_id muss eine Ganzzahl sein')

    def __str__(self) -> str:
        return f'{self._family.name.capitalize()}-{self.face.name.capitalize()}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)) and not isinstance(other, int):
            return False
        if type(other) is int:
            return self.db_id == other.db_id
        
        return other.db_id == self.db_id
    
    def __gt__(self, other: object):
        if not isinstance(other, type(self)):
            return True
        return self.db_id > other.db_id

    def __ge__(self, other: object):
        return self > other or self == other
    
    def __lt__(self, other: object):
        return not self > other and not self == other
    
    def __le__(self, other: object):
        return not self > other
    
