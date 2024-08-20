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
        self.Deck = Playerdeck()
        
    def __str__(self) -> str:
        return f'{self.name}_{self.player_id}'

    def change_gametype(self, gametype: GameType) -> None:
        for karte in self.Deck:
            karte.switch_gametype(gametype)
        self.Deck.sort(reverse=True)

if __name__ == '__main__':
    player = DokoPlayer('Player', 0)
    print(player)
    
    doko_game = []
    for i in range(4):
        doko_game.append(DokoPlayer('Player', i))
    
    for player in doko_game:
        print(player)
        
    new_cards = FullDeck()
    new_cards.shuffle_deck()
    
    for player in doko_game:
        for i in range(10):
            index = player.player_id * 10 + i
            player.Deck.append(new_cards[index])
            
    print()
    for player in doko_game:
        print(f'{player}:')
        player.Deck.sort(reverse=True)
        msg = ''
        for card in player.Deck:
            msg += f'{card} '
        print(msg)
    