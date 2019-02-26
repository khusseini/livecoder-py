from .command import Command
from livecoder.sequencer import Track


class CreateTrackCommand(Command):
    def do_run(self, track_name: str = None):
        midi_player = self.app.livecoder.midi_player
        if track_name is not None:
            self.output.info('Selecting track {}'.format(track_name))
            if not midi_player.has_track(track_name):
                num = len(midi_player.tracks) + 1
                track = Track(track_name, num)
                self.app.state.add_track(track)
                midi_player.add_track(track)
            midi_player.select_track(track_name)
            return
        tracks = []
        i = 0
        for t in midi_player.tracks:
            tracks.append("Ch.{0}: {1}".format(i, t.name))
            i += 1
        self.output.list(tracks, 'Current tracks', False, self.mark_track)

    def mark_track(self, index, item):
        selected_track = self.app.livecoder.midi_player.selected_track
        if selected_track is not None:
            return "Ch.{0}: {1}".format(index, item) == selected_track.name

        return False

    def run(self, command: str, **kwargs):
        self.do_run(**kwargs)
