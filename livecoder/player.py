from livecoder.sequencer import Sequencer


class Player:
    def __init__(self, seq: Sequencer):
        self.sequencer = seq
        self.ticks = []
        self.pos = 0
        self.playing = False
        self.length = 0

    def compile(self):
        self.ticks = self.sequencer.compile_tick_list()
        self.length = len(self.ticks)

    def start(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def stop(self):
        self.pause()
        self.pos = 0

    def tick(self, send: callable):
        if not self.playing or not len(self.ticks):
            return

        if self.pos >= self.length:
            self.pos = 0
        tick = self.ticks[self.pos]

        for tick_msg in tick:
            if tick_msg is None:
                continue
            send(tick_msg)

        self.pos += 1
