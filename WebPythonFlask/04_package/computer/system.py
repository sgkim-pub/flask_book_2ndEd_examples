from computer import CPU
from computer import RAM
from computer import VGA

class system():
    def report(self):
        return (CPU.report(), RAM.report(), VGA.report())
