from .clip import Clip


class Playable:
    is_playing = False
    dirty = True
    pos = 0
    fpb = 400
    signature = 1/4
    _compiled = []

    def set_timing(self, fpb: int = 400, signature: float = 1 / 4):
        self.signature = signature
        self.fpb = fpb
        self.dirty = True

    def length_to_ticks(self, note_length: float) -> int:
        return int(note_length * (self.fpb/self.signature))

    def ticks_to_length(self, ticks: int) -> float:
        return ticks / (self.fpb/self.signature)

    def play(self):
        self.is_playing = True

    def pause(self):
        self.is_playing = False

    def reset(self):
        self.position(0)

    def stop(self):
        self.pause()
        self.reset()

    def position(self, pos: int):
        self.pos = pos

    def get_position(self, pos: int):
        return self._compiled[pos]

    def tick(self):
        if not self.is_playing:
            return []

        if self.dirty:
            self.compile(self.fpb, self.signature)

        if self.pos > len(self._compiled):
            return []
        tick = self.get_position(self.pos)
        self.pos += 1
        return tick

    def compile(self, fpb: int = 400, signature: float = 1/4):
        self.set_timing(fpb, signature)
        self.dirty = False


class Track(Playable):
    clips: list = []
    dirty: bool = True
    sequence: list = []

    def __init__(self, name: str, channel: int):
        self.channel = channel
        self.name = name

    def add_clip(self, clip: Clip):
        self.clips.append(clip)

    def compile(self, fpb: int = 400, signature: float = 1/4):
        super(Track, self).compile(fpb, signature)

        for c in self.clips:
            self._compiled += c.compile(fpb, signature)
        return self._compiled
