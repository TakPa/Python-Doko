# -*- coding: utf-8 -*-
from DokoCards import *


class DokoPlayer:
    Deck: Playerdeck = Playerdeck()

    @property
    def name(self):
        return self._name

    @property
    def player_id(self):
        return self._id

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise ValueError('Name muss als String übergeben werden')
        if len(name) == 0:
            raise ValueError("Name darf nicht leer sein")
        self._name = name

    @player_id.setter
    def player_id(self, player_id: int):
        self._id = player_id

    def __init__(self, name: str, player_id: int) -> None:
        self.name = name
        self.player_id = player_id
        self.Deck: Playerdeck = Playerdeck()

    def __str__(self) -> str:
        return f'{self.name}_{self.player_id}'

    def init_new_game(self):
        self.Deck.clear()

    def change_game_type(self, game_type: GameType) -> None:
        for karte in self.Deck:
            karte.switch_gametype(game_type)
        self.Deck.sort(reverse=True)

    @property
    def is_re_partner(self) -> bool:
        re_dame = DokoCard(CardFamily.KREUZ, CardFace.DAME)
        return re_dame in self.Deck

    @property
    def has_hochzeit(self) -> bool:
        return len([crd for crd in self.Deck if crd.family == CardFamily.KREUZ and crd.face == CardFace.DAME]) > 1

    @property
    def has_abgabe(self) -> bool:
        matches: int = 0
        for crd in self.Deck:
            if crd.is_trumpf:
                matches += 1
                if matches > 3:
                    return False
        return True

    @property
    def has_five_kings(self) -> bool:
        return len([crd for crd in self.Deck if crd.face == CardFace.KOENIG]) > 4

    @property
    def has_ninety_points(self) -> bool:
        return sum(crd.face.value for crd in self.Deck) > 89

    @property
    def can_not_fuchs_stechen(self) -> bool:
        return len([crd for crd in self.Deck if crd.priority > (GamePriority.TRUMPF.value + CardFace.AS.value)]) == 0

    @property
    def can_schmeissen(self) -> (bool, str):
        msg_: str = "SCHMEISSEN: "
        length: int = len(msg_)

        if self.has_five_kings:
            msg_ += "FÜNF KÖNIGE "

        if self.has_ninety_points:
            msg_ += "NEUNZIG AUGEN "

        if self.can_not_fuchs_stechen:
            msg_ += "FUCHS NICHT STECHEN "

        yes_he_can = length < len(msg_)

        return yes_he_can, msg_
