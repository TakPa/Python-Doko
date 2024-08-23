from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import  QLabel, QGridLayout, QHBoxLayout

from Player import DokoPlayer
from game import Game


class PlayerWidgets():
    _layout: QGridLayout | QGridLayout
    _is_re: bool = False
    _doko_cards: list[QLabel] = []

    @property
    def player_id(self) -> int:
        return self._doko_player.player_id

    @property
    def name_label(self) -> QLabel:
        return self._name_label

    @property
    def partner_label(self) -> QLabel:
        msg = 'KONTRA'
        if self._doko_player.is_re_partner:
            if self._doko_player.has_hochzeit:
                msg = 'HOCHZEIT'
            else:
                msg = 'RE'
        self._partner_label.setText(msg)
        return self._partner_label

    @property
    def player_widgets(self) -> QGridLayout:
        return self._layout

    def __init__(self, player: DokoPlayer):
        assert (isinstance(player, DokoPlayer))
        self._doko_player = player
        self._name_label = QLabel(f'{player} :')
        self._partner_label = QLabel(f'KONTRA')
        self._abgabe_label = QLabel('')
        self._five_kings_label = QLabel('')
        self._layout = QGridLayout()
        self._build_layout(self._layout)
        self._child_layout = QHBoxLayout()
        self._build_child_layout(self._child_layout)
        self._layout.addChildLayout(self._child_layout)
        self._layout.addChildWidget(self._child_layout)

    def _build_layout(self, layout):
        layout.addWidget(self._name_label, 0, 0)
        layout.addWidget(self._partner_label, 0, 2)
        layout.addWidget(self._abgabe_label, 0, 4)
        layout.addWidget(self._five_kings_label, 0, 6)

    def _build_child_layout(self, layout):
        self._doko_cards.clear()

        for crd in self._doko_player.Deck:
            card_label = QLabel()
            card_label.setPixmap(QPixmap(crd.image))
            self._doko_cards.append(card_label)
            
            layout.addWidget(card_label)

    def update_game_infos(self):
        self._update_infos()
        self._update_card_labels()

    def _update_card_labels(self):
        for index, crd in enumerate(self._doko_player.Deck):
            self._doko_cards[index].setPixmap(QPixmap(crd.image))

    def _update_infos(self):
        msg = 'KONTRA'
        if self._doko_player.is_re_partner:
            if self._doko_player.has_hochzeit:
                msg = 'HOCHZEIT'
            else:
                msg = 'RE'
        self._partner_label.setText(msg)

        abgabe = ''
        if self._doko_player.has_abgabe:
            abgabe = ' ABGABE '
        self._abgabe_label.setText(abgabe)

        five_kings = ''
        if self._doko_player.has_five_kings:
            five_kings = 'Fünf Könige'
        self._five_kings_label.setText(five_kings)

if __name__ == '__main__':
    game = Game()
    game.new_game()
    widgets = []

    for plyer in game.playerlist:
        widgets.append(PlayerWidgets(plyer))



