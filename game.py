# -*- coding: utf-8 -*-
from typing import List, Any

from DokoCards import FullDeck, GameType
from Player import DokoPlayer
from PlayCard import CardFamily


class Game:
   
    _player_list: List[DokoPlayer] = [DokoPlayer('Player', 0),
                                      DokoPlayer('Player', 1),
                                      DokoPlayer('Player', 2),
                                      DokoPlayer('Player', 3)
                                      ]
    _player_vorbehalt: List[GameType] =[]
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
        for i in range(len(self.player_list)):
            self._player_vorbehalt.append(GameType.NORMAL) 

    def new_game(self):

        self._full_deck.shuffle_deck()
        for _player in self.player_list:
            _player.init_new_game()
            # player.Deck.clear()
            for i in range(10):
                index = _player.player_id * 10 + i
                _player.Deck.append(self._full_deck[index])
            _player.change_game_type(GameType.NORMAL, True)
            _player.Deck.sort(reverse=True)
        for game_type in self._player_vorbehalt:
            game_type = GameType.NORMAL

    def change_game_type(self, game_type: GameType):
        for plyer in self.player_list:
            plyer.change_game_type(game_type)
        self.game_type = game_type

    def handle_vorbehalt(self, game_type: GameType, player: DokoPlayer):
        self._player_vorbehalt[player.player_id] = game_type
        if game_type.value < self.game_type.value:
            return False
        
        current_vorbehalt = max([x.value for x in self._player_vorbehalt])
        if game_type.value < current_vorbehalt:
            return False
        
        current_vorbehalt_player = [self._player_vorbehalt.index(x) for x in \
                            [y for y in self._player_vorbehalt \
                            if y.value == current_vorbehalt] ]
        
        if current_vorbehalt_player[0] < player.player_id :
            return False

        self.change_game_type(game_type)
        return True        


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
