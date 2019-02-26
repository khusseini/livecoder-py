from .functions import FunctionRegistry
from .playable import Playable
import collections


class Clip(Playable):

    @property
    def value(self):
        return self._value

    @property
    def clip_fill(self):
        return self._clip_fill

    @clip_fill.setter
    def clip_fill(self, value: bool):
        self._clip_fill = value

    @property
    def clip_length(self):
        return self._clip_length

    @clip_length.setter
    def clip_length(self, value: float):
        self._clip_length = value

    def __init__(self, value: str, function_registry: FunctionRegistry = None):
        super(Clip, self).__init__()
        self._clip_length: float
        self._clip_fill: bool = False
        self._sequences: dict = collections.OrderedDict()
        self._function_registry: FunctionRegistry
        self._value: str
        self._value = value
        self.function_registry = function_registry
        self._clip_length = 0

    def _has_function(self, name: str) -> bool:
        if self.function_registry is None:
            return False
        return self.function_registry.has_function(name)

    def add_sequence(self, index, sequence: list):
        self._is_dirty = True
        self._sequences[index] = sequence

    def get_frames(self, frames_per_beat: int = 400, signature: float = 1 / 4) -> list:
        self.compile(frames_per_beat, signature)
        return self._compiled_frames

    def compile(self, frames_per_beat: int = 400, signature: float = 1 / 4):
        super(Clip, self).compile(frames_per_beat, signature)
        if not self._is_dirty:
            return self._compiled_frames
        self._is_dirty = False

        frames = []

        sequences = {}
        for note_number in self._sequences:
            items = self._sequences[note_number]
            if self._has_function(note_number):
                items = self.function_registry.call(note_number, **items)
                for nn in items:
                    if nn not in sequences:
                        sequences[nn] = []
                    sequences[nn] += items[nn]
            else:
                sequences[note_number] = items

        repeat = self._clip_fill
        clip_length = self.length_to_ticks(self._clip_length)

        for note_number in sequences:
            sequence = sequences[note_number]

            index = 0
            while True:
                for note in sequence:
                    if index == len(frames):
                        frames.append([])
                    frames[index].append(note)

                    next_index = self.length_to_ticks(note.length) + index
                    frames_to_add = max(next_index - len(frames), 0)
                    index = next_index
                    for i in range(0, frames_to_add):
                        frames.append([])
                if not repeat or index > clip_length - 1:
                    break

        self._compiled_frames = frames
        return self._compiled_frames
