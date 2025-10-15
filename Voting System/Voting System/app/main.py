
from shell.main_window import run_app
from app.core.db import init_db

if __name__ == '__main__':
    init_db()
    run_app()
