# -*- coding: utf-8 -*-

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
    
class Card:
    __slots__ = ('_family', '_face', '_image')
    ImagePath: str = 'E:/User/Projects/Python Doko/Images/'

    @classmethod
    def copy_card(cls, card):
        if not isinstance(card, Card):
            raise TypeError('card muss eine Instanz der Klasse Card sein')
        
        return Card(card.family, card.face)    
    
    @property
    def family(self):
        return self._family
   
    @property
    def face(self):
        return self._face
    
    @property
    def DB_ID(self) -> int:
        return self._family.value * 100 + self._face.value 

    @property
    def image(self):
        return f'{Card.ImagePath}{self.family.name.capitalize()}_{self.face.name.capitalize()}.gif'

    @family.setter
    def family(self, value):
        if not isinstance(value, CardFamily):
            raise TypeError('family muss eine gültige CardFamily sein')
        self._family = value
        
    @face.setter
    def face(self, value):
        if not isinstance(value, CardFace):
            raise TypeError('face muss eine gültige CardFace sein')
        self._face = value

    
    def __init__(self, family: CardFamily, face: CardFace):

        self.family = family
        self.face = face
        

    def __str__(self) -> str:
        return f'{self.family.name.capitalize()}-{self.face.name.capitalize()}'

    # noinspection PyUnresolvedReferences
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, type(self)) and not isinstance(value, type(0)):
            return False
        if type(value) == type(0):
            return self.DB_ID == value
        
        return value.DB_ID == self.DB_ID
    
    def __gt__(self, other: object):
        if not isinstance(other, type(self)) :
            return True
        return self.DB_ID > other.DB_ID

    def __ge__(self, other: object):
        return self > other or self == other
    
    
    def __lt__ (self, other: object):
        return  not self > other and not self == other 
    
    def __le__ (self, other: object):
        return  not self > other 
