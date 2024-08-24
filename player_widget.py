from PyQt6 import QtCore, QtGui, QtWidgets

from Player import DokoPlayer
from game import Game


class Players(QtWidgets.QWidget):
    players = list[DokoPlayer]
    player_widgets = []

    def __init__(self, *args, **kwargs):
        super(Players, self).__init__(*args, **kwargs)
        self.setWindowTitle("Player Widgets")
        self.game: Game = Game()
        self.game.new_game()
        self.players = self.game.playerlist

        layout = QtWidgets.QVBoxLayout()
        for i in range(len(self.players)):
            widget = PlayerWidget(doko_player=self.players[i])
            self.player_widgets.append(widget)
            layout.addWidget(widget)

        self.setLayout(layout)

    def on_new_game(self):
        self.game.new_game()
        for player in self.player_widgets:
            player.update_widgets()


class PlayerWidget(QtWidgets.QWidget):
    _doko_player: DokoPlayer

    def __init__(self, doko_player, *args, **kwargs):
        super(PlayerWidget, self).__init__(*args, **kwargs)

        self._doko_player = doko_player
        layout = QtWidgets.QVBoxLayout()

        self.header_layout = QtWidgets.QHBoxLayout()

        self._name_label = QtWidgets.QLabel((str(self._doko_player) + ' : ').upper())
        self._name_label.setStyleSheet("QLabel {font-weight: bold}")

        self._partner_label = QtWidgets.QLabel("")

        self._abgabe_label = QtWidgets.QLabel("")
        self._abgabe_label.setStyleSheet("QLabel {font-weight: bold; color : magenta; }")

        self._schmeissen_label = QtWidgets.QLabel("")
        self._schmeissen_label.setStyleSheet("QLabel {font-weight: bold; color : yellow; }")

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
        self.update_playerdeck()

    def update_header(self):
        me: DokoPlayer = self._doko_player
        label: QtWidgets.QLabel = self._partner_label

        if me.is_re_partner:
            if me.has_hochzeit:
                label.setText('HOCHZEIT')
            else:
                label.setText('RE')
        else:
            label.setText('KONTRA')

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

    def update_playerdeck(self):

        try:
            deck = self._doko_player.Deck
            layout = self.cards_layout

            for i in range(self.cards_layout.count()):
                item = self.cards_layout.itemAt(i)
                if type(item.widget()) == QtWidgets.QLabel:
                    widget = item.widget()
                    item.widget().setPixmap(QtGui.QPixmap(self._doko_player.Deck[i].image))
        except Exception as ex:
            print(f'Player {self._doko_player.player_id}:', ex)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Doppelkopf Test')
        # set the grid layout
        self.players = Players()
        #self.setStyleSheet("background-color: gainsboro; color: lightgray")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.players,0, 0, 8, 8, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        child_layout = QtWidgets.QHBoxLayout()
        button_change: QtWidgets.QPushButton = QtWidgets.QPushButton('New Game')
        # noinspection PyUnresolvedReferences
        button_change.clicked.connect(self.players.on_new_game)
        child_layout.addWidget(button_change,
                               alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.button_close = QtWidgets.QPushButton('Close')
        self.button_close.clicked.connect(self.close)
        child_layout.addWidget(self.button_close,alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addLayout(child_layout, 10, 0, 1, 10)

        layout_options = QtWidgets.QVBoxLayout()
        self.options_group = QtWidgets.QGroupBox('GAME TYPE :')

        self.option_solo1 = QtWidgets.QRadioButton('Normal')
        self.option_solo1.setStyleSheet("color: black;"
                                        "font-weight: bold;")
        self.option_solo1.toggled.connect(self.on_options_clicked)

        self.option_solo2 = QtWidgets.QRadioButton('Hochzeit')
        self.option_solo2.setStyleSheet("color: black;"
                                        "font-weight: bold;")
        self.option_solo2.toggled.connect(self.on_options_clicked)
                        
                        
        self.option_solo3 = QtWidgets.QRadioButton('Buben Solo')
        self.option_solo3.setStyleSheet("color: black;"
                                        "font-weight: bold;")
        self.option_solo3.toggled.connect(self.on_options_clicked)
        
        self.option_solo4 = QtWidgets.QRadioButton('Damen Solo')
        self.option_solo4.setStyleSheet("color: black;"
                                        "font-weight: bold;")
        self.option_solo4.toggled.connect(self.on_options_clicked)

        self.option_solo1.setChecked(True)

        layout_options.addWidget(self.option_solo1)
        
        layout_options.addWidget(self.option_solo2)
        layout_options.addWidget(self.option_solo3)
        layout_options.addWidget(self.option_solo4)

        self.options_group.setLayout(layout_options)
        self.options_group.setStyleSheet("background-color: lightyellow;"
                                         "font-weight: bold;"
                                         "border: 1px solid gray;"
                                         "margin-top: 1px")
                        
        layout.addWidget(self.options_group, 1 ,10,)

        self.setLayout(layout)

    def on_options_clicked(self):
        rb:QRadioButton = self.sender()
        if rb.isChecked():
            print(f"option {rb.text()} clicked")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    #player = Players()
    #player.show()
    app.exec()
