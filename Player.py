# -*- coding: utf-8 -*-

from DokoCards import *
from DokoCards import GameType


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
        
    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    

class DokoPlayer(Player):

    # @property
    # def name(self):
    #     return self.name

    @property
    def player_id(self):
        return self.id

    def __init__(self, name: str, player_id: int) -> None:
        super().__init__(name, player_id)
        # self._player = Player(name, player_id)
        self.Deck: PlayerDeck = PlayerDeck()
        self.game_type = GameType.NORMAL
        
        self._is_re = False
        self._can_schmeissen = [False, '']
        self._has_abgabe = False
        self._vorbehalte = []

    def __str__(self) -> str:
        return f'{self.name}_{self.player_id}'

    def init_new_game(self):
        self.Deck.clear()
        self.game_type = GameType.NORMAL
        
    def change_game_type(self, game_type_: GameType) -> None:
        self.game_type = game_type_
        self.Deck.switch_gametype(game_type_)
        self.Deck.sort(reverse=True)
        if self.game_type.is_normal_game:
            self.set_normal_game_status()
    
    def set_normal_game_status(self):
        self._can_schmeissen = self.can_schmeissen
        self._has_abgabe = self.Deck.has_abgabe
        self._is_re = self.Deck.is_re_deck

    def set_solo_game_status(self, i_am_player: bool):
        self._is_re = 1 if i_am_player else 0

    @property
    def is_re_partner(self) -> bool:
        return self._is_re > 0

    @property
    def has_hochzeit(self) -> bool:
        return self._is_re > 1

    @property
    def has_abgabe(self) -> bool:
        return self._has_abgabe

    @property
    def has_five_kings(self) -> bool:
        return self.Deck.has_five_kings

    @property
    def has_ninety_points(self) -> bool:
        return self.Deck.has_ninety_points

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
            
        if self.game_type.is_normal_game:
            if not self.can_fuchs_stechen:
                msg_ += "FUCHS NICHT STECHEN "

        yes_he_can = length < len(msg_)

        return yes_he_can, msg_
    
    def get_valid_vorbehalte(self):
        _vorbehalte = []
        _schmeissen, txt = self.can_schmeissen
        if _schmeissen:
            _vorbehalte.append(GameType.SCHMEISSEN)
        if self.has_hochzeit:
            _vorbehalte.append(GameType.HOCHZEIT)
        if self.has_abgabe:
            _vorbehalte.append(GameType.ABGABE)
        self._vorbehalte = _vorbehalte
        return self._vorbehalte
            
