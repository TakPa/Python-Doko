# -*- coding: utf-8 -*-
from DokoCards import *
from dataclasses import field

@dataclass(frozen=True)
class Player:
    _name: str
    _id: int
    
    def __post_init__(self):
        if not isinstance(self._name, str):
            raise ValueError('Name muss als String übergeben werden')
        if len(self._name) == 0:
            raise ValueError("Name darf nicht leer sein")
        if not isinstance(self._id, int):
            raise ValueError('Id muss eine Ganzzahl sein')
    
class DokoPlayer:
    Deck: PlayerDeck = PlayerDeck() 

    @property
    def name(self):
        return self._player._name

    @property
    def player_id(self):
        return self._player._id

    def __init__(self, name: str, player_id: int) -> None:
        self._player = Player(name,player_id)
        # self.name = name
        # self.player_id = player_id
        self.Deck: PlayerDeck = PlayerDeck()

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
        return self.Deck.is_re_deck > 0

    @property
    def has_hochzeit(self) -> bool:
        return self.Deck.is_re_deck > 1

    @property
    def has_abgabe(self) -> bool:
        return len([crd for crd in self.Deck if crd.is_trumpf]) < 4

    @property
    def has_five_kings(self) -> bool:
        return len([crd for crd in self.Deck if crd.face == CardFace.KOENIG]) > 4

    @property
    def has_ninety_points(self) -> bool:
        return sum(crd.face.value for crd in self.Deck) > 89

    @property
    def can_fuchs_stechen(self) -> bool:
        fuchs = DokoCard(CardFamily.KARO, CardFace.AS)
        
        fuchs_priority = fuchs.db_id + GamePriority.TRUMPF.value 
        return len([crd for crd in self.Deck if crd.priority > fuchs_priority]) > 0

    @property
    def can_schmeissen(self) -> tuple[bool, str]:
        msg_: str = "SCHMEISSEN: "
        length: int = len(msg_)

        if self.has_five_kings:
            msg_ += "FÜNF KÖNIGE "

        if self.has_ninety_points:
            msg_ += "NEUNZIG AUGEN "

        if not self.can_fuchs_stechen:
            msg_ += "FUCHS NICHT STECHEN "

        yes_he_can = length < len(msg_)

        return yes_he_can, msg_
