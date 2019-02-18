from .functions import FunctionRegistry


class Clip:
    repeats: int = 0
    clip_fill: bool = False
    sequence: list = []
    function_registry: FunctionRegistry
    dirty: bool = True
    _compiled: []
    last_signature: 0

    def __init__(self, function_registry: FunctionRegistry):
        self.function_registry = function_registry

    def add(self, object):
        self.dirty = True
        self.sequence.append(object)

    @staticmethod
    def length_to_ticks(note_length: float, signature: float, fpb: int = 400) -> int:
        return int(note_length * (fpb/signature))

    @staticmethod
    def ticks_to_length(ticks: int, signature: float, fpb: int = 400) -> float:
        return ticks / (fpb/signature)

    def get_ticks(self, signature: float = 1/4):
        if self.dirty or self.last_signature != signature:
            self._compiled = self.compile(signature)
            self.dirty = False
            self.last_signature = signature

        return self._compiled

    def compile(self, tpb: int = 400, signature: float = 1/4):
        parts = []
        max_length = 0
        for raw_step in self.sequence:
            func_name = raw_step["name"]
            part_sequences = self.function_registry.call(func_name, **{"config": raw_step["args"]})
            for p in part_sequences:
                plen = 0
                for seq in p:
                    plen += seq.length
                max_length = max(max_length, plen)
                parts.append(p)

        clip_length = self.length_to_ticks(max_length, signature, tpb)
        frames = []
        repeat = self.clip_fill

        for part in parts:
            index = 0
            while True:
                for note in part:
                    if index+1 > len(frames):
                        frames.append([])
                    frames[index].append(note)
                    frames_to_add = self.length_to_ticks(note.length, signature, tpb)
                    added_index = 0
                    for i in range(1, frames_to_add):
                        added_index = i + index
                        if added_index+1 > len(frames):
                            frames.append([])
                    index = added_index+1
                if not repeat or index > clip_length-1:
                    break
        return frames
