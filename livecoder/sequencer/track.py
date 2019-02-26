from .clip import Clip
from .playable import Playable


class Track(Playable):
    @property
    def clips(self):
        return self._clips

    def __init__(self, name: str, channel: int):
        super(Track, self).__init__()
        self.channel = channel
        self.name = name
        self._clips: list = []

    def add_clip(self, clip: Clip):
        self._is_dirty = True
        self._clips.append(clip)

    def compile(self, frames_per_beat: int = 400, signature: float = 1 / 4):
        super(Track, self).compile(frames_per_beat, signature)
        if not self._is_dirty:
            return self._compiled_frames
        self._is_dirty = False

        for c in self._clips:
            self._compiled_frames += c.compile(frames_per_beat, signature)

        return self._compiled_frames
