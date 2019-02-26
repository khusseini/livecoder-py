from livecoder.sequencer.note import Note
from .sequencer_function import SequencerFunction


class Drums(SequencerFunction):
    map: dict = {
        'k': 44,
        'sn': 45,
        'hhc': 46,
        'hho': 47,
    }

    def __init__(self):
        super().__init__('drums')

    def run(self, **kwargs):
        return self.do_run(**kwargs)

    def do_run(self, groups: dict, **kwargs):
        sequence = {}
        for group_name in groups:
            if group_name not in self.map:
                raise ValueError("DrumFunction does not support `{0}`".format(group_name))
            note_number = self.map[group_name]
            sequence[note_number] = []
            for s in groups[group_name]:
                if s["is_pause"]:
                    note = Note(-1)
                else:
                    note = Note(note_number)
                note.length = float(s["length"])
                sequence[note_number].append(note)
        return sequence

