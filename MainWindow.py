from PyQt6.QtCore import pyqtSlot
from PyQt6 import QtWidgets, QtCore

from player_widget import Players
# from game_option_widget import OptionBox

from DokoCards import GameType
from game import Game, DokoPlayer


class MainWindow(QtWidgets.QMainWindow):

    @pyqtSlot(DokoPlayer, GameType)
    def player_game_type_changed(self,  player: DokoPlayer, game_type: GameType):
        print(game_type, player)
        player.vorbehalt_type = game_type
        self.game.handle_vorbehalt(game_type, player)
        if self.game.game_type is game_type:
            print('accepted', self.game.game_type) 
        else:
            print('rejected', game_type, 'current:', self.game.game_type) 
         
        self.players.update_widgets()
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game: Game = Game()
        self.game.new_game()

        self.setGeometry(100, 100, 500, 300)

        self.title = 'Doppelkopf Test'

        self.setWindowTitle('Doppelkopf Test')
        self.players = Players(self.game)
        self.players.vorbehalt.connect(self.player_game_type_changed)
        self.central_widget = QtWidgets.QWidget(self)
        
        # self.central_widget.setStyleSheet("background-color: gainsboro; color: lightgray")
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.players, 0, 0, 9, 8, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        child_layout = QtWidgets.QHBoxLayout()
        button_change: QtWidgets.QPushButton = QtWidgets.QPushButton('New Game')
        # button_change.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")
        # noinspection PyUnresolvedReferences
        button_change.clicked.connect(self.on_new_game_clicked)
        child_layout.addWidget(button_change,
                               alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.button_close = QtWidgets.QPushButton('Close')
        # self.button_close.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")

        # noinspection PyUnresolvedReferences
        self.button_close.clicked.connect(self.close)
        child_layout.addWidget(self.button_close, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addLayout(child_layout, 10, 0, 1, 11)

        # self.option_box = OptionBox('GameType :')
        # self.option_box.setStyleSheet("background-color: gainsboro;"
        #   "color: navy;"
        #   "font-weight: bold;"
        #   "border: 1px solid gray;"
        #   "margin-top: 8px")

        # self.option_box.game_type_changed.connect(self.game_type_changed)
        # layout.addWidget(self.option_box, 2, 10)

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
                 
    def on_new_game_clicked(self):
        self.game.new_game()
        self.players.update_widgets()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # from PyQt6.QtWidgets import QStyleFactory
    # print(QStyleFactory.keys())
    # print(app.style().objectName())
    # app.setStyleSheet('windowsvista')
    window = MainWindow()
    window.show()
    app.exec()
