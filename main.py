import sys
from src.models import create_app, MainWindow


if __name__ == "__main__":
    app = create_app()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())