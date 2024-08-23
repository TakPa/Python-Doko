from PyQt6.QtWidgets import  QLabel, QGridLayout, QHBoxLayout

from Player import DokoPlayer
from game import Game


class Players_Header():

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
    def player_layout(self):
        return self._layout
    
    def __init__(self, player: DokoPlayer):
        assert (isinstance(player, DokoPlayer))
        self._doko_player = player
        self._name_label = QLabel(f'{player} :')
        self._partner_label = QLabel(f'KONTRA')
        self._abgabe_label = QLabel('')
        self._five_kings_label = QLabel('')
        self._layout = QHBoxLayout()
        self._build_layout(self._layout)
        self.update_infos()
        
    def _build_layout(self, layout):
        layout.addWidget(self._name_label)
        layout.addWidget(self._partner_label)
        layout.addWidget(self._abgabe_label)
        layout.addWidget(self._five_kings_label)

        '''
        layout.addWidget(self._name_label, 0, 0, 0, 2)
        layout.addWidget(self._partner_label, 0, 2, 0, 2)
        layout.addWidget(self._abgabe_label, 0, 4, 0, 2)
        layout.addWidget(self._five_kings_label, 0, 6, 0, 2)
        '''        

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

        five_kings = ''
        if self._doko_player.has_five_kings:
            five_kings = 'Fünf Könige'
        self._five_kings_label.setText(five_kings)

