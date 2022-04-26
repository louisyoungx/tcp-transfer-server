from Core.core import run
from Core.sendTrack import track
from Settings import debug

if __name__ == "__main__":
    if not debug:
        run()
    else:
        track()