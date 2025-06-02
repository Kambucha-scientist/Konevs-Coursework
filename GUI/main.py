import sys
from main_window import MainWindow

from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    # Установка стиля
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()