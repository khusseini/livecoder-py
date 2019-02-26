from livecoder.sequencer import Track
from livecoder.sequencer import Playable
import mido


class MidiPlayer(Playable):
    def __init__(self, output: mido.ports.IOPort = None):
        super(MidiPlayer, self).__init__()
        self._tracks: list = []
        self._output: mido.ports.IOPort
        self._selected_track: Track
        self._output = output
        self.notes_sent = {}
        self._selected_track = None
        self._repeat = True

    @property
    def tracks(self):
        return self._tracks

    @property
    def selected_track(self):
        return self._selected_track

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output: mido.ports.IOPort):
        self._output = output

    @property
    def position(self) -> int:
        return super(MidiPlayer, self).position

    @position.setter
    def position(self, value: int):
        self._position = value
        for t in self._tracks:
            t.position = value

    def has_track(self, track_name: str) -> bool:
        for t in self._tracks:
            if t.name == track_name:
                return True
        return False

    def add_track(self, track: Track):
        self._tracks.append(track)

    def select_track(self, name: str):
        t = None
        for track in self._tracks:
            if track.name == name:
                t = track
        if t is not None:
            self._selected_track = t
        return t

    def compile(self, frames_per_beat: int = 400, signature: float = 1 / 4):
        super(MidiPlayer, self).compile(frames_per_beat, signature)
        for track in self._tracks:
            track.compile(frames_per_beat, signature)
        self._is_dirty = False

    def play(self):
        super(MidiPlayer, self).play()
        for t in self._tracks:
            t.play()

    def stop(self):
        super(MidiPlayer, self).stop()
        for t in self._tracks:
            t.stop()

    def pause(self):
        super(MidiPlayer, self).pause()
        for t in self._tracks:
            t.pause()

    def get_track(self, name: str):
        for t in self._tracks:
            if t.name == name:
                return t

    def get_channel(self, name: str):
        index = 0
        for t in self._tracks:
            if t.name == name:
                return index
            index += 1

    def get_frame(self):
        if not self._is_playing:
            return []
        if self.is_dirty:
            self.compile(self._frames_per_beat, self._signature)
        self._position += 1

        current_position = self.position - 1
        notes_on = {}
        notes_off = {}
        max_length = 0
        messages = []

        # Prepare notes_off
        for track_name in self.notes_sent:
            notes_sent = self.notes_sent[track_name]
            for note in notes_sent[:]:
                if current_position - note["start"] == self.length_to_ticks(note["n"].length)-1:
                    self.notes_sent[track_name].remove(note)
                    if track_name not in notes_off:
                        notes_off[track_name] = []
                    notes_off[track_name].append(note["n"])

        # Prepare notes on
        for track in self._tracks:
            notes_on[track.name] = track.get_frame()

        # Process notes_off
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

        # Process notes_on
        for track_name in notes_on:
            if track_name not in self.notes_sent:
                self.notes_sent[track_name] = []

            for note in notes_on[track_name]:
                max_length = max(note.length, max_length)
                if note.number >= 0:
                    self.notes_sent[track_name].append({"n": note, "start": current_position})
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
        if self._output:
            for msg in messages:
                self._output.send(msg)
        return messages
