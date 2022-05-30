from Storage import storage
from Config import config

from .transfer import transfer
from .track import track

def main():
    if not config.Debug.open:
        transfer()
    else:
        track()


