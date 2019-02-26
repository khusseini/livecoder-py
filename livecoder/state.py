from collections import namedtuple
import livecoder.sequencer as ls

MidiIO = namedtuple('int', ['input', 'output'])
Clip = namedtuple('str', ["name", "body"])


class Track:
    def __init__(self, name: str, channel: str, clips: list):
        self.name = name
        self.channel = channel
        self.clips = clips


class State():
    _selected_io: MidiIO
    _tracks: list
    _clips: list
    _commands: list

    def __init__(self):
        self._selected_io = MidiIO(0, 0)
        self._tracks = []
        self._clips = []
        self._commands = []

    def add_command(self, command: str):
        self._commands.append(command)

    def add_clip(self, clip: Clip):
        self._clips.append(clip)

    def add_track(self, track: ls.Track):
        clips = []
        for clip in track.clips:
            clips.append(Clip(name=clip.value, body=clip.value))
        self._tracks.append(Track(name=track.name, channel=track.channel, clips=clips))
