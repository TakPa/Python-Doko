import sys
from PyQt6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout

from game_option_widget import OptionBox, GameType

class VorbehalteDialog(QDialog):
    
    def __init__(self):
        super().__init__()

        self.game_type = GameType.NORMAL    
        self.setWindowTitle("Vorbehalt")

    
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        

        layout = QVBoxLayout()
        self.option_box = OptionBox('')
        self.option_box.game_type_changed.connect(self.on_game_type_changed)
        
        layout.addWidget(self.option_box)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def on_game_type_changed(self, game_type):
        self.game_type = game_type
        print(f'{str(game_type)} received')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VorbehalteDialog()
    window.show()
    app.exec()
            