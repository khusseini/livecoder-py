class Playable:
    def __init__(self):
        self._compiled_frames: list = []
        self._frames_per_beat: int = 400
        self._is_dirty: bool = True
        self._is_playing: bool = False
        self._position: int = 0
        self._signature: float = 1 / 4
        self._repeat: bool = True

    @property
    def is_dirty(self):
        return self._is_dirty

    @property
    def signature(self) -> float:
        return self._signature

    @signature.setter
    def signature(self, value: float):
        self._is_dirty = self._is_dirty or self.signature != value
        self._signature = value

    @property
    def frames_per_beat(self) -> int:
        return self._frames_per_beat

    @frames_per_beat.setter
    def frames_per_beat(self, value: float):
        self._is_dirty = self._is_dirty or self.frames_per_beat != value
        self._frames_per_beat = value

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, pos: int):
        self._position = pos

    def length_to_ticks(self, note_length: float) -> int:
        return int(note_length * (self._frames_per_beat / self._signature))

    def ticks_to_length(self, ticks: int) -> float:
        return ticks / (self._frames_per_beat / self._signature)

    def play(self):
        self._is_playing = True

    def pause(self):
        self._is_playing = False

    def reset(self):
        self._position = 0

    def stop(self):
        self.pause()
        self.reset()

    def get_frame(self):
        if not self._is_playing:
            return []
        if self._is_dirty:
            self.compile(self._frames_per_beat, self._signature)
        if self._position >= len(self._compiled_frames):
            if not self._repeat:
                return []
            self._position = 0
        tick = self._compiled_frames[self._position]
        self._position += 1
        return tick

    def compile(self, frames_per_beat: int = 400, signature: float = 1 / 4):
        self.frames_per_beat = frames_per_beat
        self.signature = signature
