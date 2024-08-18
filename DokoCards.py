# -*- coding: utf-8 -*-
from PlayingCards import *
from enum import Enum, unique
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
        return self == GameType.NORMAL or self == GameType.NORMAL or self == GameType.NORMAL


class DokoCard(Card):
    __slots__ = ('_priority', '_is_trumpf')

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

    def __init__(self, family: CardFamily, face: CardFace) -> None:
        super().__init__(family, face)
        self._priority: int = 0
        self._is_trumpf: bool = False
        self.switch_gametype(GameType.NORMAL)

    def switch_gametype(self, gametype=GameType.NORMAL):
        """

        :type gametype: GameType
        """
        priority = self.DB_ID

        if gametype != GameType.NONE:
            if gametype.is_normal_game:
                if self.family == CardFamily.HERZ and self.face == CardFace.ZEHN:
                    priority += GamePriority.DULLE.value
                elif self.face == CardFace.DAME:
                    priority += GamePriority.DAME.value
                elif self.face == CardFace.BUBE:
                    priority += GamePriority.BUBE.value
                elif self.family == CardFamily.KARO:
                    priority += GamePriority.TRUMPF.value
            elif gametype == GameType.DAMEN_SOLO and self.face == CardFace.DAME:
                priority += GamePriority.DAME.value
            elif gametype == GameType.BUBEN_SOLO and self.face == CardFace.BUBE:
                priority += GamePriority.BUBE.value

        self.priority = priority
        self.is_trumpf = self.priority > GamePriority.TRUMPF.value

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
    def __init__(self, iterable : UserList[DokoCard] = None):
        data: UserList[DokoCard] = iterable

        if data == None:
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
        newdeck = random.sample(self.data, k=40)
        return DokoDeck(newdeck)

    def shuffle_deck(self):
        random.shuffle(self.data)


class FullDeck(DokoDeck):
    def __init__(self):
        data : UserList[DokoCard] = UserList()
        for family in CardFamily:
            for face in CardFace:
                data.append(DokoCard(family, face))
                data.append(DokoCard(family, face))
        super().__init__(data)
        #self.data.sort(reverse=True)

    def shuffle_deck(self):
        random.shuffle(self.data)

class Playerdeck(DokoDeck):

    def __init__(self):
        super().__init__()

    def switch_gametype(self, gametype : GameType):
        for dokocard  in self.data:
            dokocard.switch_gametype(gametype)



if __name__ == '__main__':

    fulldeck = FullDeck()
    fulldeck.shuffle_deck()

    playerdecks = []
    for i in range(4):
        playerdecks.append([])

    for i in range(4):
        playerdecks[i].clear()
        for y in range(10):
            playerdecks[i].append(fulldeck[(i * 10) + y])

    for i in range(4):
        playerdecks[i].sort(reverse=True)
        playerdeck = ''
        for card in playerdecks[i]:
            playerdeck += f'{card}; '
        print(playerdeck)
