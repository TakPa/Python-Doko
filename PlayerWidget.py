from typing import List, Any

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QGridLayout, QHBoxLayout

from Player import DokoPlayer


class PlayersHeader():
    Karten: List[QLabel] = []

    @property
    def player_layout(self):
        return self._layout

    def __init__(self, player: DokoPlayer):
        assert (isinstance(player, DokoPlayer))
        self._doko_player = player
        self._name_label = QLabel(f'{player} :')
        self._name_label.setStyleSheet("QLabel {font-weight: bold}")
        self._partner_label = QLabel(f'KONTRA')

        self._abgabe_label = QLabel('')
        self._abgabe_label.setStyleSheet("QLabel {font-weight: bold; color : red; }")

        self._schmeissen_label = QLabel('')
        self._schmeissen_label.setStyleSheet("QLabel {font-weight: bold; color : yellow; }")

        for index in range(len(self._doko_player.Deck)):
            self.Karten.append(QLabel())

        self._layout = QHBoxLayout()
#        self._layout = QGridLayout()
        self._build_layout(self._layout)

        self.update_infos()
        self.update_card_elements()

    def _build_layout(self, layout):
        layout.addWidget(self._name_label)
        layout.addWidget(self._partner_label)
        layout.addWidget(self._abgabe_label)
        layout.addWidget(self._schmeissen_label)

    def update_infos(self):
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

        schmeissen_message = ''
        (can_schmeissen, message) = self._doko_player.can_schmeissen

        if can_schmeissen:
            schmeissen_message = message
        self._schmeissen_label.setText(schmeissen_message)

    def update_card_elements(self):
        for index, crd in enumerate(self._doko_player.Deck):
            self.Karten[index].setPixmap(QPixmap(crd.image))
