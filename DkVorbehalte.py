from Player import GameType, DokoPlayer

class Player_Vorbehalt():
    def __init__(self, player: DokoPlayer) -> None:
        self._player = player
        self.reset()
        
    def reset(self):
        self._vorbehalt = GameType.NONE
        self._is_accepted = False

    @property
    def player_id(self):
        return self._player.player_id
    
    @property
    def vorbehalt(self, is_accepted = True):
        if is_accepted and not self._is_accepted:
            return GameType.NONE
        return self._vorbehalt
    
    @vorbehalt.setter
    def vorbehalt(self, vorbehalt: GameType, is_accepted: bool):
        self._vorbehalt = vorbehalt
        self.set_vorbehalt(is_accepted)
        
    def set_vorbehalt(self, is_accepted: bool):
        self._is_accepted = is_accepted


