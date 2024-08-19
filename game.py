# -*- coding: utf-8 -*-
from typing import List, Dict, Any

from DokoCards import DokoDeck, FullDeck, GameType
from Player import DokoPlayer
from PlayingCards import CardFamily


class Game:
    _playerlist: list[DokoPlayer]
    _fulldeck : FullDeck
    _game_type: GameType

    @property
    def playerlist(self):
        return self._playerlist

    @property
    def fulldeck(self):
        return self._fulldeck

    @property
    def game_type(self):
        return self._game_type

    @playerlist.setter
    def playerlist(self, iterable: List[DokoPlayer]):
        self._playerlist = iterable


    @game_type.setter
    def game_type(self, new_type:GameType):
        self._game_type = new_type
    def __init__(self):
        self._fulldeck : FullDeck = FullDeck()
        self._fulldeck.sort(reverse=True)

        self.playerlist  = self._create_playerlist()
        self.game_type = GameType.NORMAL

    def _create_playerlist(self):
        playerlist = []
        i: int

        for i in range(4):
            playerlist.append(DokoPlayer('Player', i))
        return playerlist

    def new_game(self):

        self._fulldeck.shuffle_deck()
        for player in self.playerlist:
            player.Deck.clear()
            for i in range(10):
                index = player.player_id * 10 + i
                player.Deck.append(self._fulldeck[index])
            player.Deck.sort(reverse=True)

    def change_gametype(self, gametype: GameType):
        for player in self.playerlist:
            player.change_gametype(gametype)
        self.game_type = gametype



if __name__ == '__main__':
    game = Game()
    print(game.game_type)

    for player in game.playerlist:
        print(f'{player}')
    print()

    for card in game.fulldeck:
        print(f'{card} {card.priority}')
    print()

    game.new_game()
    for player in game.playerlist:
        print(f'{player} :')

        str_deck : str = ''
        for card in player.Deck:
            str_deck += f'{card} '
        print(str_deck)
        trumpf_count = sum(map(lambda karte: karte.is_trumpf == True, player.Deck))
        count_family: list[dict[Any, Any]] = []
        for family in  CardFamily:
            count = sum(map(lambda karte: karte.family == family and karte.is_trumpf == False, player.Deck))
            if count > 0:
                count_family.append({family.name.capitalize() : count})
        print(f'Anzahl Trumpf: {trumpf_count}')
        print(f'Anzahl Fehl: {count_family}')
        print()

    game.change_gametype(GameType.BUBEN_SOLO)
    print("""
    *******************************************
    Bubensolo:
    *******************************************
    """)
    for player in game.playerlist:
        print(f'{player}: ')
        for card in player.Deck:
            print(f'{card} : {card.priority} {card.is_trumpf}')
        print()

    for player in game.playerlist:
        print(f'{player} :')

        str_deck : str = ''
        for card in player.Deck:
            str_deck += f'{card} '
        print(str_deck)
        trumpf_count = sum(map(lambda karte: karte.is_trumpf == True, player.Deck))
        count_family: list[dict[Any, Any]] = []
        for family in  CardFamily:
            count = sum(map(lambda karte: karte.family == family and karte.is_trumpf == False, player.Deck))
            if count > 0:
                count_family.append({family.name.capitalize() : count})
        print(f'Anzahl Trumpf: {trumpf_count}')
        print(f'Anzahl Fehl: {count_family}')
        print()

    print()








