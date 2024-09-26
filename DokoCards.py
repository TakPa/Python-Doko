# -*- coding: utf-8 -*-
from PlayCard import *
import random
from collections import UserList


@unique
class GamePriority(Enum):
    TRUMPF = 1000
    BUBE = 2000
    DAME = 3000
    DULLE = 5000


@unique
class GameType(Enum):
    NONE = 0
    NORMAL = 1
    HOCHZEIT = 2
    BUBEN_SOLO = 3
    DAMEN_SOLO = 4
    ABGABE = 5

    @property
    def is_normal_game(self) -> bool:
        return self == GameType.NORMAL or self == GameType.HOCHZEIT or self == GameType.ABGABE
        

class DokoCard():
    __slots__ = ('_priority', '_is_trumpf', '_karte')

    @property
    def family(self):
        return self._karte.family
    
    @property
    def face(self):
        return self._karte.face
    
    @property
    def db_id(self):
        return self._karte.db_id
    
    @property
    def image(self):
        return self._karte.image
    
    @property
    def is_Re_Dame(self):
        return self.family is CardFamily.KREUZ and self.face is CardFace.DAME
            
    @property
    def priority(self):
        return self._priority

    @property
    def is_trumpf(self):
        return self._is_trumpf

    @priority.setter
    def priority(self, value):
        self._priority = value

    @is_trumpf.setter
    def is_trumpf(self, value):
        self._is_trumpf = value

    def __init__(self, _family: CardFamily, _face: CardFace) -> None:
        # super().__init__(_family, _face)
        self._karte = PLayCard(_family, _face, _family.value * 10 + _face.value)
        self._priority: int = 0
        self._is_trumpf: bool = False
        self.switch_gametype(GameType.NORMAL)
    
    def switch_gametype_normal(self):
        if self.family == CardFamily.HERZ and self.face == CardFace.ZEHN:
            return GamePriority.DULLE.value
        if self.face == CardFace.DAME:
            return GamePriority.DAME.value
        if self.face == CardFace.BUBE:
            return GamePriority.BUBE.value
        if self.family == CardFamily.KARO:
            return GamePriority.TRUMPF.value
        return 0
            
    def switch_gametype_buben_solo(self):
        if self.face == CardFace.BUBE:
            return GamePriority.BUBE.value
        return 0

    def switch_gametype_damen_solo(self):
        if self.face == CardFace.DAME:
            return GamePriority.DAME.value
        return 0

    def switch_gametype(self, gametype=GameType.NORMAL):
        priority = self.db_id

        if gametype is GameType.NONE:
            self.priority = priority
            self.is_trumpf = False
            return

        match gametype:
            case GameType.BUBEN_SOLO:
                priority += self.switch_gametype_buben_solo()
            case GameType.DAMEN_SOLO:
                priority += self.switch_gametype_damen_solo()
            case _:
                priority += self.switch_gametype_normal()
                        
        self.priority = priority
        self.is_trumpf = self.priority > GamePriority.TRUMPF.value

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, type(self)):
            return False
        return self.db_id == value.db_id
        
    def __gt__(self, other: object):
        if not isinstance(other, type(self)):
            return True
        return self.priority > other.priority

    def __ge__(self, other: object):
        return self > other or self == other

    def __lt__(self, other: object):
        return not self > other and not self == other

    def __le__(self, other: object):
        return not self > other


class DokoDeck(UserList[DokoCard]):
    def __init__(self, iterable: UserList[DokoCard] = None):
        data: UserList[DokoCard] = iterable

        if data is None:
            data = UserList[DokoCard]

        super().__init__(item for item in data)

    def __setitem__(self, index, item):
        self.data[index] = item

    def insert(self, index, item):

        self.data.insert(index, item)

    def append(self, item):
        self.data.append(item)

    def extend(self, other):
        if isinstance(other, type(self)):
            self.data.extend(other)

    def init_fulldeck(self):
        self.data.clear()
        for family in CardFamily:
            for face in CardFace:
                self.data.append(DokoCard(family, face))
                self.data.append(DokoCard(family, face))

    def shuffle(self):
        new_deck = random.sample(self.data, k=40)
        return DokoDeck(new_deck)

    def shuffle_deck(self):
        random.shuffle(self.data)


class FullDeck(DokoDeck):
    def __init__(self, sort_order=True):
        data: UserList[DokoCard] = UserList()
        for family in CardFamily:
            for face in CardFace:
                data.append(DokoCard(family, face))
                data.append(DokoCard(family, face))
        super().__init__(data)
        self.data.sort(reverse=sort_order)

    def shuffle_deck(self):
        random.shuffle(self.data)


class PlayerDeck(DokoDeck):

    def __init__(self):
        super().__init__()

    def switch_gametype(self, gametype: GameType):
        for dokocard in self.data:
            dokocard.switch_gametype(gametype)
    
    @property 
    def is_re_deck(self):
        return len([crd for crd in self 
                     if crd.is_Re_Dame])
    @property 
    def has_abgabe(self):
        return len([crd for crd in self if crd.is_trumpf]) < 4


