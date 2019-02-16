import mido
import livecoder.midi as midi
import collections


class Track:
    def __init__(self, name: str, channel: int):
        self.channel = channel
        self.name = name
        self.track = mido.MidiTrack()
        self.fpb = mido.midifiles.midifiles.DEFAULT_TICKS_PER_BEAT

    def append(self, message_type: str, **kwargs):
        msg = midi.create_message(message_type, **kwargs)
        self.track.append(msg)

    def append_notes(self, note_length: float, notes: list = []):
        if len(notes):
            offsets = self.fetch_offsets(notes)
            last_index = len(self.track) - 1
            first_offset = next(iter(offsets))

            if last_index >= 0 and first_offset < 0:
                self.update_last_time(first_offset, True)

            self.append_offsets(offsets, 'note_on')
            self.update_last_time(note_length)
            self.append_offsets(offsets, 'note_off')
            self.update_last_time(1/(4*self.fpb), True)
            return

        self.update_last_time(note_length)

    def append_offsets(self, offsets, action: str):
        for group in offsets:
            group = offsets[group]
            for n in group:
                msg = midi.create_message(
                    action,
                    channel=self.channel,
                    note=n.number,
                    velocity=n.velocity
                )
                self.track.append(msg)

    def update_last_time(self, pause_length: float, append=False):
        ticks = int(self.length_to_ticks(pause_length))
        self.update_last_tick(ticks, append)

    def update_last_tick(self, ticks: int, append=False):
        last_index = len(self.track) - 1
        if last_index < 0:
            return
        time = ticks
        if append and self:
            time = self.track[last_index].time
            time += ticks

        self.track[last_index].time = time

    def length_to_ticks(self, note_length: float) -> int:
        return int(note_length * (self.fpb * 4))

    def ticks_to_length(self, ticks: int) -> float:
        return ticks / (4*self.fpb)

    @staticmethod
    def fetch_offsets(notes: list) -> collections.OrderedDict:
        offsets = {}
        for n in notes:
            if n.offset not in offsets:
                offsets[n.offset] = []
            if n not in offsets[n.offset]:
                offsets[n.offset].append(n)

        return collections.OrderedDict(sorted(offsets.items(), key=lambda t: t[0]))


class Sequencer:
    def __init__(
            self,
            bpm: int = 110,
            frames_per_beat: int = mido.midifiles.midifiles.DEFAULT_TICKS_PER_BEAT
    ):
        self.tracks = {}
        self.fpb = frames_per_beat
        self.bpm = bpm
        self.selected_track_name = ''

    def selected_track(self) -> Track:
        if not len(self.tracks):
            self.create_track('default', 0)

        return self.tracks[self.selected_track_name]

    def select_track(self, name: str):
        if name not in self.tracks:
            raise ValueError("{} is not a track".format(name))
        self.selected_track_name = name

    def length_to_ticks(self, note_length: float):
        return int(note_length * (self.fpb * 4))

    def create_track(self, name: str, channel: int) -> Track:
        if name not in self.tracks:
            self.tracks[name] = Track(name, channel, self)
        self.selected_track_name = name
        return self.tracks[name]

    def export_file(self) -> mido.MidiFile:
        mf = mido.MidiFile()
        for t in self.tracks:
            mf.tracks.append(self.tracks[t].track)
        return mf

    def compile_tick_list(self):
        ticks = []

        for t in self.tracks:
            track = self.tracks[t].track
            ticks.append([])
            pos = 0

            for msg in track:
                ticks[pos].append(msg)
                if msg.time <= 0:
                    continue
                note_length = track.ticks_to_length(msg.time)
                msg.time = self.length_to_ticks(note_length)
                pos = msg.time-1
                time = pos
                if time == 0:
                    time += 1
                for x in range(0, time):
                    ticks.append([])
                pos = len(ticks)-1

        return ticks
