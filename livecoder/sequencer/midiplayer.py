from livecoder.sequencer import Track
from livecoder.sequencer import Playable
import mido


class MidiPlayer(Playable):
    tracks: list = []
    output: mido.ports.IOPort
    selected_track: Track

    def __init__(self, output: mido.ports.IOPort = None):
        super(MidiPlayer, self).__init__()
        self.output = output
        self.notes_sent = {}
        self.selected_track = None

    def set_output(self, output: mido.ports.IOPort):
        self.output = output

    def has_track(self, track_name: str) -> bool:
        for t in self.tracks:
            if t.name == track_name:
                return True
        return False

    def add_track(self, track: Track):
        self.tracks.append(track)

    def select_track(self, name: str):
        t = None
        for track in self.tracks:
            if track.name == name:
                t = track
        if t is not None:
            self.selected_track = t
        return t

    def compile(self, fpb: int = 400, signature: float = 1/4):
        super(MidiPlayer, self).compile(fpb, signature)
        for track in self.tracks:
            track.compile(fpb, signature)

    def play(self):
        super(MidiPlayer, self).play()
        for t in self.tracks:
            t.play()

    def stop(self):
        super(MidiPlayer, self).stop()
        for t in self.tracks:
            t.stop()

    def pause(self):
        super(MidiPlayer, self).pause()
        for t in self.tracks:
            t.pause()

    def position(self, pos: int):
        super(MidiPlayer, self).position(pos)
        for t in self.tracks:
            t.position(pos)

    def get_track(self, name: str):
        for t in self.tracks:
            if t.name == name:
                return t

    def get_channel(self, name: str):
        index = 0
        for t in self.tracks:
            if t.name == name:
                return index
            index += 1

    def tick(self):
        if not self.is_playing:
            return []

        if self.dirty:
            self.compile(self.fpb, self.signature)
        if self.pos > len(self._compiled):
            return []

        notes_on = {}
        notes_off = {}
        max_length = 0
        messages = []

        for track_name in self.notes_sent:
            while len(self.notes_sent[track_name]):
                note = self.notes_sent[track_name].pop(0)
                if self.pos - note["start"] == note["n"].length:
                    if track_name not in notes_off:
                        notes_off[track_name] = []
                    notes_off[track_name].append(note["n"])

        for track in self.tracks:
            notes_on[track.name] = track.tick()

        for track_name in notes_off:
            for note in notes_off[track_name]:
                if note.number >= 0:
                    messages.append(
                        mido.Message(
                            'note_off',
                            note=note.number,
                            channel=self.get_channel(track_name)
                        )
                    )

        for track_name in notes_on:
            if track_name not in self.notes_sent:
                self.notes_sent = []
            for note in notes_on[track_name]:
                max_length = max(note.length, max_length)
                if note.number >= 0:
                    self.notes_sent[track_name] = note
                    messages.append(
                        mido.Message(
                            'note_on',
                            note=note.number,
                            velocity=note.velocity,
                            time=0,
                            channel=self.get_channel(track_name)
                        )
                    )
        if not len(messages):
            return []

        messages[-1].time = self.length_to_ticks(max_length)
        for msg in messages:
            self.output.send(msg)
        return messages
