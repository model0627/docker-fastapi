import sys
sys.path.append('/code/app/')

from core.config import app

if __name__ == "__main__":
    app.run()  # type: ignore
