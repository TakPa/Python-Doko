import sys
from ctypes import windll

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QComboBox 

from game import *
import PlayerWidget


class MainWindow(QWidget):
    Karten: List[QLabel] = []
    cbox: QComboBox
    Player: List[PlayerWidget.PlayersHeader] = []
    
    @property
    def game(self):
        return self._game


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Doppelkopf Test')
        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        self._game = Game()
        self._game.new_game()

        self.init_card_labels()
        self.update_card_labels()

        plyer: DokoPlayer
        for plyer in self.game.playerlist:
            self.Player.append(PlayerWidget.PlayersHeader(plyer))
            
            
            name: str = f'{plyer} :'
            row: int = plyer.player_id * 3
            child_layout = self.Player[plyer.player_id].player_layout
            layout.addLayout(self.Player[plyer.player_id].player_layout, row, 0, 2, 8)
            
            for index in range(len(plyer.Deck)):
                layout.addWidget(self.Karten[plyer.player_id * 10 + index], row + 2, index)

        # buttons
        button_change: QPushButton = QPushButton('New Game')
        # noinspection PyUnresolvedReferences
        button_change.clicked.connect(self.on_new_game)
        layout.addWidget(button_change, 14, 0, 1, 2,
                         alignment=Qt.AlignmentFlag.AlignLeft)

        button_close: QPushButton = QPushButton('Close')
        # noinspection PyUnresolvedReferences
        button_close.clicked.connect(self.on_close)
        layout.addWidget(button_close, 14, 9,
                         alignment=Qt.AlignmentFlag.AlignRight)

        self.cbox = QComboBox()
        for game_type in GameType:
            self.cbox.addItem(game_type.name, userData=game_type)
        self.cbox.setCurrentIndex(self.game.game_type.value)
        # noinspection PyUnresolvedReferences
        self.cbox.activated.connect(self.on_activated)
        layout.addWidget(QLabel('Game Type :'), 0, 11)
        layout.addWidget(self.cbox, 0, 12)

        self.show()

    def init_labels(self):
        pass
    
    def init_card_labels(self):
        for index in range(len(self.game.playerlist) * len(self.game.playerlist[0].Deck)):
            self.Karten.append(QLabel())

    def update_card_labels(self):
        for i in range(len(self.game.playerlist)):
            for j, crd in enumerate(self.game.playerlist[i].Deck):
                index = i * 10 + j
                self.Karten[index].setPixmap(QPixmap(crd.image))

    def update_player_labels(self):
        for player in self.Player:
            player.update_infos()
            
    def on_new_game(self):
        game_type = GameType[self.cbox.currentText()]
        if game_type != GameType.NORMAL:
            self.cbox.setCurrentIndex(GameType.NORMAL.value)
            if not game_type.is_normal_game:
                self.on_activated(GameType.NORMAL.value)

        self.game.new_game()
        self.update_player_labels()
        self.update_card_labels()

    def on_close(self):
        self.close()

    def on_activated(self, index: int):
        current_game_type = self.game.game_type
        new_game_type = GameType[self.cbox.currentText()] 

#        for gt in GameType:
#            if gt.value == index:
#                new_game_type = gt
#                break
 
        if new_game_type != current_game_type:
            self.game.change_gametype(new_game_type)
            self.update_card_labels()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        window = MainWindow()

        sys.exit(app.exec())
