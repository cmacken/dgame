from PyQt5.QtGui import QPixmap


{
    "player"     : "C:\\Users\\camth\\Development\\dgame\\assets\\player.png",
    "location"   : 
}


class Character:

    def __init__(self, name, icon=''):

        self.icon = QPixmap("assets/player.png").scaled(32, 32)