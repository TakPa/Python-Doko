from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal

# from Player import DokoPlayer
from game import *
from vorbehalt import VorbehalteDialog


class Players(QtWidgets.QWidget):
    players = list[DokoPlayer]
    player_widgets = []
    
    vorbehalt = pyqtSignal(DokoPlayer, GameType)

    def __init__(self, game_, *args, **kwargs):
        super(Players, self).__init__(*args, **kwargs)
        self.setWindowTitle("Player Widgets")
        self.game: Game = game_
        # self.game.new_game()
        self.players = self.game.player_list

        layout = QtWidgets.QVBoxLayout()
        for i in range(len(self.players)):
            widget = PlayerWidget(doko_player=self.players[i])
            widget.vorbehalt.connect(self.on_vorbehalt)
            self.player_widgets.append(widget)
            layout.addWidget(widget)

        self.setLayout(layout)

    def update_widgets(self):
        for player_ in self.player_widgets:
            player_.update_widgets()

    def on_vorbehalt(self, player, game_type):
        print(str(player) + ': ' + str(game_type))
        self.vorbehalt.emit(player,game_type)
        

class PlayerWidget(QtWidgets.QWidget):
    _doko_player: DokoPlayer
    
    vorbehalt = pyqtSignal(DokoPlayer, GameType)

    def __init__(self, doko_player, *args, **kwargs):
        super(PlayerWidget, self).__init__(*args, **kwargs)

        self._doko_player = doko_player
        layout = QtWidgets.QVBoxLayout()

        self.header_layout = QtWidgets.QHBoxLayout()

        self._name_label = QtWidgets.QLabel((str(self._doko_player) + ' : ').upper())
        # self._name_label.setStyleSheet("font-weight: bold; color : navy; ")

        self._partner_label = QtWidgets.QLabel("")
        # self._partner_label.setStyleSheet("font-weight: bold; color : navy; ")

        self._abgabe_label = QtWidgets.QLabel("")
        # self._abgabe_label.setStyleSheet("font-weight: bold; color : maroon; ")

        self._schmeissen_label = QtWidgets.QLabel("")
        # self._schmeissen_label.setStyleSheet("font-weight: bold; color : darkmagenta; ")

        button_style = "color: red; " + \
        "border-style: outset; " + \
        "border-width: 2px; " + \
        "border-radius: 10px; " + \
        "border-color: navy; " + \
        "font: bold ; " + \
        "min-width: 5em; " 

        self._vorbehalt_checkbox = QtWidgets.QCheckBox('Vorbehalt')
        self._vorbehalt_checkbox.checkStateChanged.connect(self.on_vorbehalt_checkbox)
        # self._vorbehalt_checkbox.setStyleSheet("font-weight: bold; color : black; "  
        #                                      "background-color : thistle; "
        #                                      "indicator{color  : navy} ")
        
        self._vorbehalt_dropdown = QtWidgets.QComboBox()
        self.update_dropdown(False)
        # self._vorbehalt_dropdown.insertItem(1000, GameType.NORMAL.name)
        # self._vorbehalt_dropdown.insertSeparator(1000)

        # valid_options = self._doko_player.get_valid_vorbehalte()
        
        # if len(valid_options) > 0:
        #     for game_type in valid_options:
        #         self._vorbehalt_dropdown.insertItem(1000, game_type.name)
        # index = len(valid_options) + 2
        # self._vorbehalt_dropdown.insertSeparator(2000)
        # self._vorbehalt_dropdown.insertItems(2000,[GameType.BUBEN_SOLO.name, GameType.DAMEN_SOLO.name])
        
        
        self._vorbehalt_dropdown.setVisible(False)
        self._vorbehalt_dropdown.currentIndexChanged.connect(self.on_index_changed)    
        self._vorbehalt_dropdown.currentTextChanged.connect(self.on_text_changed)    
        self.header_layout.addWidget(self._name_label)
        self.header_layout.addWidget(self._partner_label)

        self.header_layout.addWidget(self._vorbehalt_checkbox)
        self.header_layout.addWidget(self._vorbehalt_dropdown)
        

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

    def on_text_changed(self, s):
        print(str(f'Activierter Text: {s}'))
        print(GameType[s])
        self.vorbehalt.emit(self._doko_player,GameType[s])
        

    def on_index_changed(self, index):
        print(str(f'Activierter Index: {index}'))
        
    def on_vorbehalt(self):
        if type(self.sender()) is QtWidgets.QPushButton:
            bt = self.sender()
            if bt.isChecked():
                dlg = VorbehalteDialog()
                dlg.setWindowTitle('Vorbehalt')
                if dlg.exec():
                    game_type = dlg.game_type
                    self.vorbehalt.emit(self._doko_player,game_type)
                else:
                # noinspection PyUnresolvedReferences
                    self.vorbehalt.emit(self._doko_player,GameType.NORMAL)
    
    def on_vorbehalt_checkbox(self):
        bt = self._vorbehalt_checkbox
        if bt.isChecked():
            self._vorbehalt_dropdown.setVisible(True)
            self._vorbehalt_dropdown.showPopup()
            # dlg = VorbehalteDialog()
            # dlg.setWindowTitle('Vorbehalt')
            # if dlg.exec():
            #     game_type = dlg.game_type
            #     self.vorbehalt.emit(self._doko_player,game_type)
        else:
            # noinspection PyUnresolvedReferences
            self._vorbehalt_dropdown.setVisible(False)
            self.vorbehalt.emit(self._doko_player,GameType.NORMAL)
            bt.setChecked(False)
            
    def update_widgets(self):
        self.update_header()
        self.update_player_deck()

    def update_header(self):
        me: DokoPlayer = self._doko_player
        self._vorbehalt_checkbox.checkStateChanged.disconnect()
        
        self._vorbehalt_checkbox.setChecked(False)
        label: QtWidgets.QLabel = self._partner_label

        if me.is_re_partner:
            if me.has_hochzeit:
                label.setText('HOCHZEIT')
            else:
                label.setText('RE')

            # self._partner_label.setStyleSheet("font-weight: bold; color : green; ")
        else:
            label.setText('KONTRA')
            # self._partner_label.setStyleSheet("font-weight: bold; color : cornflowerblue; ")

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
        self.update_dropdown(True)
        self._vorbehalt_checkbox.checkStateChanged.connect(self.on_vorbehalt_checkbox)

    def update_dropdown(self, disconnect):

        if disconnect:
            self._vorbehalt_dropdown.currentIndexChanged.disconnect()    
            self._vorbehalt_dropdown.currentTextChanged.disconnect()    
        
        self._vorbehalt_dropdown.clear()
        
        self._vorbehalt_dropdown.addItem(GameType.NORMAL.name)
        self._vorbehalt_dropdown.insertSeparator(2)

        valid_options = self._doko_player.get_valid_vorbehalte()
        
        if len(valid_options) > 0:
            for game_type in valid_options:
                self._vorbehalt_dropdown.addItem(game_type.name)
        self._vorbehalt_dropdown.insertSeparator(2000)
        self._vorbehalt_dropdown.insertItems(2000,[GameType.BUBEN_SOLO.name, GameType.DAMEN_SOLO.name])
        self._vorbehalt_dropdown.currentIndexChanged.connect(self.on_index_changed)    
        self._vorbehalt_dropdown.currentTextChanged.connect(self.on_text_changed)    
        
    def update_player_deck(self):
        try:
            for i in range(self.cards_layout.count()):
                item = self.cards_layout.itemAt(i)
                if type(item.widget()) == QtWidgets.QLabel:
                    # noinspection PyUnresolvedReferences
                    item.widget().setPixmap(QtGui.QPixmap(self._doko_player.Deck[i].image))
        except Exception as ex:
            print(f'Player {self._doko_player.player_id}:', ex)
