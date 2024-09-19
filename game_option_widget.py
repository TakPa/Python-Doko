
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from DokoCards import GameType


class OptionBox(QtWidgets.QGroupBox):
 
    game_types = {
        'Normal': GameType.NORMAL,
        'Hochzeit': GameType.HOCHZEIT,
        'Buben_Solo': GameType.BUBEN_SOLO,
        'Damen_Solo': GameType.DAMEN_SOLO,
        'Abgabe': GameType.ABGABE
    }
    
    @pyqtSlot(GameType)
    def type_changed_received(self, gametype):
        print('game type changed received')
    
    def on_game_type_changed(self,gametype):
        if type(self.sender()) is QtWidgets.QRadioButton:
            rb = self.sender()
            if rb.isChecked():
                self.game_type_changed.emit(GameType[rb.text().upper()])
    
    game_type_changed = QtCore.pyqtSignal(GameType, name='game_type_changed')    
    
    
    option_button: list[QtWidgets.QRadioButton] = []

    def __init__(self, titel):
        super().__init__(titel)
        

        options = self.game_types.keys()
        self.option_button.clear()
        self.setTitle(titel)
        self.setStyleSheet(
                                         "color: navy;"
                                         "font-weight: bold;"
                                         "border: 3px solid gray;"
                                          "margin-top: 8px")
        for index, key in enumerate(options):
            button = QtWidgets.QRadioButton(key)
            button.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")
            # noinspection PyUnresolvedReferences
            self.option_button.append(button)
        self.option_button[0].setChecked(True)
        
        options_layout =QtWidgets.QVBoxLayout()
        for button in self.option_button:
            button.toggled.connect(self.on_options_toggled)
            button.toggled.connect(self.on_game_type_changed)
            options_layout.addWidget(button)

        self.setLayout(options_layout)
        self.game_type_changed.connect(self.game_type_changed)        
        
    def on_options_toggled(self):
        if type(self.sender()) is QtWidgets.QRadioButton:
            rb = self.sender()
            if rb.isChecked():
                
                print(f"Game Type {GameType[rb.text().upper()]} clicked")
                self.game_type_changed.emit(GameType[rb.text().upper()])
                print (f'{GameType[rb.text().upper()]} emitted')

        

    """         self.setStyleSheet("background-color: rebeccapurple;"
                                         "color: red;"
                                         "font-weight: bold;"
                                         "border: 1px solid gray;"
                                         "margin-top: 1px")
    """

    def init_options(self):
        options = self.game_types.keys()
        self.option_button.clear()
        for index, key in enumerate(options):
            button = QtWidgets.QRadioButton(key)
            button.setStyleSheet("background-color: moccasin; color: black; font-weight: bold;")
            # noinspection PyUnresolvedReferences
            self.option_button.append(button)
            self.option_group.addWidget(self.option_button[index])
            


