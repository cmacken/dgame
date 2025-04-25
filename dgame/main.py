import sys
from dgame.core.gui.main_window import MainWindow
from dgame.core.controller import GameController
from dgame.core.world.manager import WorldManager
from PyQt5.QtWidgets import QApplication
import time

def main():
    app = QApplication(sys.argv)
    controller = GameController()
    wman = WorldManager()
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec_())

def test_terminal():
    controller = GameController()
    while True:
        controller.update()
        time.sleep(1)



if __name__ == '__main__':

    #main()
    test_terminal()