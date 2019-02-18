import re

note_map = {
    'C': 60,
    'D': 62,
    'E': 64,
    'F': 65,
    'G': 67,
    'A': 69,
    'B': 71,
    'H': 71
}

note_regex = re.compile('([a-g])([#b])?(-?[1-9])?', re.IGNORECASE)


class Note:
    def __init__(self, number: int):
        self.number = number
        self.velocity = 64
        self.offset = 0
        self.length = 0


def from_string(name: str, offset: int = -3) -> Note:
    result = note_regex.match(name)
    if not result:
        raise ValueError(name + " is not a supported notation")

    mod = 0
    if result.group(2) == 'b':
        mod = -1
    elif result.group(2) == '#':
        mod = 1

    octave = offset + 1

    if result.group(3):
        octave = int(result.group(3)) + offset

    note = note_map[result.group(1).capitalize()] + (octave * 12) + mod

    return Note(note)
