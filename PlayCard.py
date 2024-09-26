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
    family: CardFamily
    face: CardFace
    db_id: int
    image_path: str = 'E:/User/Projects/Python Doko/Images/'
    
    @property
    def image(self):
        return f'{self.image_path}{self.family.name.capitalize()}' + \
                f'_{self.face.name.capitalize()}.gif'

    def __post_init__(self):
        if not isinstance(self.family, CardFamily):
            raise ValueError('family muss Kartenfamile sein (KREUZ, PIK, ... ) ')
        if not isinstance(self.face, CardFace):
            raise ValueError('face muss Kartengesicht sein (AS, ZEHN, ... ) ')
        if not isinstance(self.db_id, int):
            raise ValueError('db_id muss eine Ganzzahl sein')

    def __str__(self) -> str:
        return f'{self.family.name.capitalize()}-{self.face.name.capitalize()}'

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, type(self)) and not isinstance(value, type(0)):
            return False
        if type(value) is type(0):
            return self.db_id == value
        
        return value.db_id == self.db_id
    
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
    
