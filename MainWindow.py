from PyQt6.QtCore import pyqtSlot
from PyQt6 import QtWidgets, QtCore


from player_widget import Players
from game_option_widget import OptionBox

from DokoCards import GameType
from game import Game


class MainWindow(QtWidgets.QMainWindow):
    option_buttons: list[QtWidgets.QRadioButton] = []

    @pyqtSlot(GameType)
    def game_type_changed(self, game_type):
        print(f'pyqtSlot: signal received: {game_type}')
        self.game.change_gametype(game_type)
        self.players.update_widgets()
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game: Game = Game()
        self.game.new_game()

        self.setGeometry(100, 100, 500, 300)

        self.title = 'Doppelkopf Test'
        self.filters = 'Text Files (*.txt)'

        # container = QWidget(self)
        self.setWindowTitle('Doppelkopf Test')
        # set the grid layout
        self.players = Players(self.game)
        self.central_widget = QtWidgets.QWidget(self)
        
        self.central_widget.setStyleSheet("background-color: gainsboro; color: lightgray")
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.players, 0, 0, 8, 8, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        child_layout = QtWidgets.QHBoxLayout()
        button_change: QtWidgets.QPushButton = QtWidgets.QPushButton('New Game')
        button_change.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")
        # noinspection PyUnresolvedReferences
        button_change.clicked.connect(self.on_new_game_clicked)
        child_layout.addWidget(button_change,
                               alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.button_close = QtWidgets.QPushButton('Close')
        self.button_close.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")

        # noinspection PyUnresolvedReferences
        self.button_close.clicked.connect(self.close)
        child_layout.addWidget(self.button_close, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addLayout(child_layout, 10, 0, 1, 11)

        options_layout = QtWidgets.QVBoxLayout()

        for key in GameType:
            if key is not GameType.NONE:
                option_string = key.name.capitalize()
                button = QtWidgets.QRadioButton(option_string)
                button.setStyleSheet("background-color: plum; color: black;")
                # noinspection PyUnresolvedReferences
                button.toggled.connect(self.on_options_clicked)
                if key is GameType.NORMAL:
                    button.setChecked(True)
                options_layout.addWidget(button)
                
        self.options_group = QtWidgets.QGroupBox('Game Type :')
        self.options_group.setLayout(options_layout)
        self.options_group.setStyleSheet("background-color: navy;"
                                         "color: white;"
                                         "font-weight: bold;"
                                         "border: 3px solid gray;"
                                         "margin-top: 8px")

        # noinspection PyUnresolvedReferences
        self.options_group.toggled.connect(self.on_options_clicked)
        layout.addWidget(self.options_group, 1, 10,)
        
        self.option_box = OptionBox('GameType :')
        self.option_box.setStyleSheet("background-color: navy;"
                                      "color: white;"
                                      "font-weight: bold;"
                                      "border: 3px solid gray;"
                                      "margin-top: 8px")

        self.option_box.game_type_changed.connect(self.game_type_changed)

        layout.addWidget(self.option_box, 3, 10,)

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
                 
    def on_options_clicked(self):
        rb: QtWidgets.QRadioButton

        if type(self.sender()) is QtWidgets.QRadioButton:
            rb: QtWidgets.QRadioButton = self.sender()
            if rb.isChecked():
                print(f"Game Type {GameType[rb.text().upper()]} clicked")
    
    def on_new_game_clicked(self):
        self.game.new_game()
        self.players.update_widgets()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
