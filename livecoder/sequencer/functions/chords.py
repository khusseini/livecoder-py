import re
from livecoder.sequencer.note import Note
from .sequencer_function import SequencerFunction

interval_map = {
    'i': 0,
    'ii': 1,
    'iii': 2,
    'iv': 3,
    'v': 4,
    'vi': 5,
    'vii': 6
}

default_mods = {
    'i': 'maj',
    'ii': 'm',
    'iii': 'm',
    'iv': 'maj',
    'v': 'maj',
    'vi': 'm',
    'vii': 'dim'
}

chord_mods = {
    'maj':      (0,          4,       7               ),
    'maj7':     (0,          4,       7,            11),
    'maj9':     (0,    2,    4,       7,            11),
    'maj11':    (0,          4, 5,    7,            11),
    'maj13':    (0,          4,       7,    9,      11),
    'maj9#11':  (0,    2,    4,       7,            11),
    'maj13#11': (0,          4,    6,       9,      11),
    '6':        (0,          4,       7,    9,        ),
    'add9':     (0,    2,    4,       7,            11),
    '6add9':    (0,    2,    4,       7,    9,        ),
    'maj7b5':   (0,          4,    6,               11),
    'maj7#5':   (0,          4,          8,         11),
    'm':        (0,       3,          7               ),
    'm7':       (0,       3,          7,        10,   ),
    'm9':       (0,    2, 3,          7,        10,   ),
    'm11':      (0,       3,    5, 6,           10,   ),
    'm13':      (0,       3,          7,    9,  10,   ),
    'm6':       (0,       3,          7,    9,        ),
    'madd9':    (0,    2, 3,          7,        10,   ),
    'm6add9':   (0,    2, 3,          7,    9,        ),
    'mmaj7':    (0,       3,          7,            11),
    'mmaj9':    (0,    2, 3,          7,            11),
    'm7b5':     (0,       3,       6,           10,   ),
    'm7#5':     (0,       3,             8,     10,   ),
    '7':        (0,          4,       7,        10,   ),
    '9':        (0,    2,    4,       7,        10,   ),
    '11':       (0,          4, 5,    7,        10,   ),
    '13':       (0,          4,       7,    9,  10,   ),
    '7sus4':    (0,             5,    7,        10,   ),
    '7b5':      (0,          4,    6,           10,   ),
    '7#5':      (0,          4,          8,     10,   ),
    '7b9':      (0, 1,       4,       7,            11),
    '7#9':      (0,       3,          7,        10,   ),
    '7(b5,b9)': (0, 1,       4,    6,               11),
    '7(b5,#9)': (0,       3,       6,           10,   ),
    '7(#5,b9)': (0, 1,       4,          8,         11),
    '7(#5,#9)': (0,       3,             8,     10,   ),
    '9b5':      (0,    2,    4,    6,           10,   ),
    '9#5':      (0,    2,    4,          8,     10,   ),
    '13#11':    (0,          4, 5,    7,    9,      11),
    '13b9':     (0, 1,       4,       7,    9,        ),
    '11b9':     (0, 1,       4, 5,    7,              ),
    'aug':      (0,          4,          8,           ),
    'dim':      (0,       3,       6                  ),
    'dim7':     (0,       3,       6,       9,        ),
    '5':        (0,                   7,              ),
    'sus4':     (0,             5,    7,              ),
    'sus2':     (0,    2,             7,              ),
    'sus2sus4': (0,    2,       5,    7,              ),
    '-5':       (0,       3,             8,           )
}

interval_regex = re.compile('^(iv|i{1,3}|vi{0,2})(.*)$')


class Chords(SequencerFunction):
    def __init__(self, scale: list = [0, 2, 4, 5, 7, 9, 11]):
        super().__init__(interval_regex)
        self._scale = scale
        self._key_note = Note(60)

    def run(self, **kwargs):
        return self.do_run(**kwargs)

    @property
    def key_note(self):
        return self._key_note

    @key_note.setter
    def key_note(self, note: Note):
        self._key_note = note

    def do_run(self, called_name: str, groups: dict):
        matches = interval_regex.match(called_name)
        index = matches.group(1)
        mod = matches.group(2)
        if not mod:
            mod = default_mods[index]
        pitches = self.get_notes(index, mod)

        notes = {}
        index = 0
        for pitch in pitches:
            if pitch.number not in notes:
                notes[pitch.number] = []

            group_rhythm = groups.get(str(index), groups.get("_", []))
            index += 1

            for rhythm in group_rhythm:
                note_number = pitch.number
                if rhythm["is_pause"]:
                    note_number = -1

                note = Note(note_number, rhythm["length"])
                notes[pitch.number].append(note)

        return notes

    def get_notes(self, index, mod) -> list:
        key = self.key_note
        root = key.number + self._scale[interval_map[index]]
        mod = chord_mods[mod]
        notes = []
        if not mod:
            mod = []

        for m in mod:
            note = Note(root + m)
            notes.append(note)

        return notes
