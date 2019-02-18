from livecoder.sequencer.note import Note
from .function import Function


class DrumFunction(Function):
    map: dict = {
        'k': 60,
        'hho': 61,
        'hhc': 62,
        'sn': 64
    }

    def __init__(self, map: dict = {}):
        if len(map) > 0:
            self.map = map
        super(DrumFunction, self).__init__('drums', self.do_run)

    def do_run(self, config: list):
        seq = []
        for n in config:
            seq.append([])
            if n["name"] not in self.map:
                raise ValueError("DrumFunction does not support `{0}`".format(n["name"]))
            note_number = self.map[n["name"]]
            for s in n["seq"]:
                if s["is_pause"]:
                    note = Note(-1)
                else:
                    note = Note(note_number)
                note.length = float(s["length"])
                seq[-1].append(note)
        return seq

