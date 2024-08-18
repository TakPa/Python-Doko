import sys
from ctypes import windll

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout

from game import *
import DokoCards


class MainWindow(QWidget):

    @property
    def game(self):
        return self._game

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._game = Game()
        self._game.new_game()

        self.setWindowTitle('Doppelkopf Test')

        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        plyer: DokoPlayer
        for plyer in self.game.playerlist:
            name: str = f'{plyer} :'
            row: int = plyer.player_id * 2
            layout.addWidget(QLabel(name), row, 0)

            crd: DokoCards.Card
            for index, crd in enumerate(plyer.Deck):
                cards_image: str = crd.image

                image = QLabel()
                px = QPixmap(cards_image)

                #                px = icon.pixmap(QSize(72,96))
                px.depth()
                w = int(px.width())
                h = int(px.height())

#                pixmap = px.scaled(w, h, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
                pixmap = px.scaled(w, h)

                image.setPixmap(pixmap)
                layout.addWidget(image, row + 1, index)
                layout.addWidget(image, row + 1, index)

        '''        
        # username
        #layout.addWidget(QLabel('Username:'), 0, 0)
        #layout.addWidget(QLineEdit(), 0, 1)

        # password
        #layout.addWidget(QLabel('Password:'), 1, 0)
        #layout.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 1, 1)

        # buttons
        #layout.addWidget(QPushButton('Log in'), 2, 0,
        #                 alignment=Qt.AlignmentFlag.AlignRight)
        #layout.addWidget(QPushButton('Close'), 2, 1,
        #                alignment=Qt.AlignmentFlag.AlignRight)

        # show the window
        '''

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        window = MainWindow()

        sys.exit(app.exec())
