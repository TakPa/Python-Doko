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
        if not isinstance(player_id, int):
            raise ValueError("ID muss numerisch sein")
        self.name = name
        self.player_id = player_id
        self.Deck: Playerdeck = Playerdeck()

    def __str__(self) -> str:
        return f'{self.name}_{self.player_id}'

    def init_new_game(self):
        self.Deck.clear()

    def change_gametype(self, gametype: GameType) -> None:
        for karte in self.Deck:
            karte.switch_gametype(gametype)
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
        message: str = "SCHMEISSEN: "
        length: int = len(message)
        yes_he_can: bool = False

        if self.has_five_kings:
            message += "FÜNF KÖNIGE "

        if self.has_ninety_points:
            message += "NEUNZIG AUGEN "

        if self.can_not_fuchs_stechen:
            message += "FUCHS NICHT STECHEN "

        yes_he_can = length < len(message)

        return yes_he_can, message


if __name__ == '__main__':

    doko_game = []
    for i in range(4):
        doko_game.append(DokoPlayer('Player', i))

    for player in doko_game:
        print(player)

    new_cards = FullDeck()
    new_cards.shuffle_deck()

    for player in doko_game:
        player.init_new_game()
        for i in range(10):
            index = player.player_id * 10 + i
            player.Deck.append(new_cards[index])

    print()
    for player in doko_game:
        player.Deck.sort(reverse=True)
        partner = 'KONTRA'
        if player.is_re_partner:
            if player.has_hochzeit:
                partner = 'HOCHZEIT'
            else:
                partner = 'RE'

        abgabe = ''
        if player.has_abgabe:
            abgabe = ' ABGABE '

        five_kings = ''
        (can_schmeissen, message) = player.can_schmeissen

        if can_schmeissen:
            five_kings = message

        # if player.has_five_kings:
        #     five_kings = 'Fünf Könige'

        msg = ''
        for card in player.Deck:
            msg += f'{card} '

        print(f'{player}:  {partner}  {abgabe}  {five_kings}')
        print(msg)
