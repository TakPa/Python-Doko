from PyQt6.QtCore import pyqtSlot
from PyQt6 import QtWidgets, QtCore


from player_widget import Players
from game_option_widget import OptionBox

from DokoCards import GameType


class MainWindow(QtWidgets.QMainWindow):
    option_buttons: list[QtWidgets.QRadioButton] = []

    @pyqtSlot(GameType)
    def game_type_changed(self,gametype):
        print (f'signal received: {gametype}')
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(100, 100, 500, 300)
        m = 30

        self.title = 'Doppelkopf Test'
        self.filters = 'Text Files (*.txt)'

        #container = QWidget(self)
        self.setWindowTitle('Doppelkopf Test')
        # set the grid layout
        self.players = Players()
        self.central_widget = QtWidgets.QWidget(self)
        
        self.central_widget.setStyleSheet("background-color: gainsboro; color: lightgray")
        

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.players,0, 0, 8, 8, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        child_layout = QtWidgets.QHBoxLayout()
        button_change: QtWidgets.QPushButton = QtWidgets.QPushButton('New Game')
        button_change.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")
        # noinspection PyUnresolvedReferences
        button_change.clicked.connect(self.players.on_new_game)
        child_layout.addWidget(button_change,
                               alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.button_close = QtWidgets.QPushButton('Close')
        self.button_close.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")

        # noinspection PyUnresolvedReferences
        self.button_close.clicked.connect(self.close)
        child_layout.addWidget(self.button_close,alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addLayout(child_layout, 10, 0, 1, 11)

        options_layout =QtWidgets.QVBoxLayout()

        for key in GameType:
            if key is not GameType.NONE:
                option_string = key.name.capitalize()
                button = QtWidgets.QRadioButton(option_string)
                button.setStyleSheet("background-color: plum; color: black;")
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

        self.options_group.toggled.connect(self.on_options_clicked)
        layout.addWidget(self.options_group, 1 ,10,)
        
        self.optionbox = OptionBox('GameType :')
        self.optionbox.setStyleSheet("background-color: navy;"
                                         "color: white;"
                                         "font-weight: bold;"
                                         "border: 3px solid gray;"
                                          "margin-top: 8px")

        self.optionbox.game_type_changed.connect(self.game_type_changed)

        layout.addWidget(OptionBox('GameType :'), 3 ,10,)

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
                 
    
    def on_options_clicked(self):
        rb:QtWidgets.QRadioButton

        if type(self.sender()) is QtWidgets.QRadioButton:
            rb = self.sender()
            if rb.isChecked():
                print(f"Game Type {GameType[rb.text().upper()]} clicked")
                
    def option_box_toggled(game_type):
        print(f'game type from option box : {str(game_type)}')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
