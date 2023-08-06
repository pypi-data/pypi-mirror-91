from time import sleep

class Clock():
    def __init__(self):
        self._running=True
    def terminate(self):
        self._running=False
    def run(self, n):
        i=n
        while (self._running and i!=0):
            sleep(1)
            i-=1