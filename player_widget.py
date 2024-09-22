from PyQt6 import QtGui, QtWidgets

# from Player import DokoPlayer
from game import *


class Players(QtWidgets.QWidget):
    players = list[DokoPlayer]
    player_widgets = []

    def __init__(self, game_, *args, **kwargs):
        super(Players, self).__init__(*args, **kwargs)
        self.setWindowTitle("Player Widgets")
        self.game: Game = game_
        # self.game.new_game()
        self.players = self.game.player_list

        layout = QtWidgets.QVBoxLayout()
        for i in range(len(self.players)):
            widget = PlayerWidget(doko_player=self.players[i])
            self.player_widgets.append(widget)
            layout.addWidget(widget)

        self.setLayout(layout)

    def update_widgets(self):
        for player_ in self.player_widgets:
            player_.update_widgets()


class PlayerWidget(QtWidgets.QWidget):
    _doko_player: DokoPlayer

    def __init__(self, doko_player, *args, **kwargs):
        super(PlayerWidget, self).__init__(*args, **kwargs)

        self._doko_player = doko_player
        layout = QtWidgets.QVBoxLayout()

        self.header_layout = QtWidgets.QHBoxLayout()

        self._name_label = QtWidgets.QLabel((str(self._doko_player) + ' : ').upper())
        self._name_label.setStyleSheet("font-weight: bold; color : navy; ")

        self._partner_label = QtWidgets.QLabel("")
        self._partner_label.setStyleSheet("font-weight: bold; color : navy; ")

        self._abgabe_label = QtWidgets.QLabel("")
        self._abgabe_label.setStyleSheet("font-weight: bold; color : maroon; ")

        self._schmeissen_label = QtWidgets.QLabel("")
        self._schmeissen_label.setStyleSheet("font-weight: bold; color : darkmagenta; ")

        self.header_layout.addWidget(self._name_label)
        self.header_layout.addWidget(self._partner_label)
        self.header_layout.addWidget(self._abgabe_label)
        self.header_layout.addWidget(self._schmeissen_label)

        layout.addLayout(self.header_layout)

        self.cards_layout = QtWidgets.QHBoxLayout()

        for i in range(10):
            card_widget = QtWidgets.QLabel()
            card_widget.setPixmap(QtGui.QPixmap(''))
            self.cards_layout.addWidget(card_widget)

        layout.addLayout(self.cards_layout)
        self.setLayout(layout)
        self.update_widgets()

    def update_widgets(self):
        self.update_header()
        self.update_player_deck()

    def update_header(self):
        me: DokoPlayer = self._doko_player
        label: QtWidgets.QLabel = self._partner_label

        if me.is_re_partner:
            if me.has_hochzeit:
                label.setText('HOCHZEIT')
            else:
                label.setText('RE')

            self._partner_label.setStyleSheet("font-weight: bold; color : green; ")
        else:
            label.setText('KONTRA')
            self._partner_label.setStyleSheet("font-weight: bold; color : cornflowerblue; ")

        label = self._abgabe_label
        if me.has_abgabe:
            label.setText('ABGABE')
        else:
            label.setText("")

        label = self._schmeissen_label

        schmeissen_message = ''
        (can_schmeissen, message) = self._doko_player.can_schmeissen

        if can_schmeissen:
            schmeissen_message = message
        label.setText(schmeissen_message)

    def update_player_deck(self):
        try:
            for i in range(self.cards_layout.count()):
                item = self.cards_layout.itemAt(i)
                if type(item.widget()) == QtWidgets.QLabel:
                    # noinspection PyUnresolvedReferences
                    item.widget().setPixmap(QtGui.QPixmap(self._doko_player.Deck[i].image))
        except Exception as ex:
            print(f'Player {self._doko_player.player_id}:', ex)
