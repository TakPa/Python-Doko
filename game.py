# -*- coding: utf-8 -*-
from typing import List, Any

from DokoCards import FullDeck, GameType
from Player import DokoPlayer
from PlayingCards import CardFamily


class Game:
   
    _player_list: List[DokoPlayer] = [DokoPlayer('Player', 0),
                                      DokoPlayer('Player', 1),
                                      DokoPlayer('Player', 2),
                                      DokoPlayer('Player', 3),
                                      ]
    _full_deck: FullDeck = FullDeck()

    @property
    def player_list(self):
        return self._player_list

    @property
    def full_deck(self):
        return self._full_deck

    @property
    def game_type(self):
        return self._game_type

    @player_list.setter
    def player_list(self, iterable: List[DokoPlayer]):
        self._player_list = iterable

    @game_type.setter
    def game_type(self, new_type: GameType):
        self._game_type = new_type
    
    def __init__(self):
        self.game_type = GameType.NORMAL

    def new_game(self):

        self._full_deck.shuffle_deck()
        for _player in self.player_list:
            _player.init_new_game()
            # player.Deck.clear()
            for i in range(10):
                index = _player.player_id * 10 + i
                _player.Deck.append(self._full_deck[index])
            _player.change_game_type(GameType.NORMAL)
            _player.Deck.sort(reverse=True)

    def change_game_type(self, game_type: GameType):
        for plyer in self.player_list:
            plyer.change_game_type(game_type)
        self.game_type = game_type


if __name__ == '__main__':
    game = Game()

    print(game.game_type)

    for player in game.player_list:
        print(f'{player}')
    print()

    for card in game.full_deck:
        print(f'{card} {card.priority}')
    print()

    game.new_game()
    for player in game.player_list:
        print(f'{player} :')

        str_deck: str = ''
        for card in player.Deck:
            str_deck += f'{card} '
        print(str_deck)
        trumpf_count = sum(map(lambda karte: karte.is_trumpf, player.Deck))
        count_family: list[dict[Any, Any]] = []
        for family in CardFamily:
            count = sum(map(lambda karte: karte.family == family and not karte.is_trumpf, player.Deck))
            if count > 0:
                count_family.append({family.name.capitalize(): count})
        print(f'Anzahl Trumpf: {trumpf_count}')
        print(f'Anzahl Fehl: {count_family}')
        print()

    game.change_game_type(GameType.BUBEN_SOLO)
    print("""
    *******************************************
    Bubensolo:
    *******************************************
    """)
    for player in game.player_list:
        print(f'{player}: ')
        for card in player.Deck:
            print(f'{card} : {card.priority} {card.is_trumpf}')
        print()

    for player in game.player_list:
        print(f'{player} :')

        str_deck: str = ''
        for card in player.Deck:
            str_deck += f'{card} '
        print(str_deck)
        trumpf_count = sum(map(lambda karte: karte.is_trumpf, player.Deck))
        count_family: list[dict[Any, Any]] = []
        for family in CardFamily:
            count = sum(map(lambda karte: karte.family == family and not karte.is_trumpf, player.Deck))
            if count > 0:
                count_family.append({family.name.capitalize(): count})
        print(f'Anzahl Trumpf: {trumpf_count}')
        print(f'Anzahl Fehl: {count_family}')
        print()

    print()
