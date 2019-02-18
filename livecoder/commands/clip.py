from .command import Command
from .command import Output
from .command import Application
from livecoder.parser import Parser
from livecoder.sequencer import Clip
import livecoder.sequencer.functions as func


class CreateClipCommand(Command):
    parser: Parser
    function_registry: func.FunctionRegistry

    def __init__(self, app: Application, output: Output):
        super(CreateClipCommand, self).__init__(app, output)
        self.parser = Parser()
        self.function_registry = func.FunctionRegistry([func.DrumFunction])

    def create_clip(self):
        return Clip(self.function_registry)

    def do_run(self, clip_string:str, track_name: str = None):
        track = self.app.livecoder.midi_player.selected_track
        if track_name is not None:
            track = self.app.livecoder.midi_player.select_track(track_name)
        if track is None:
            self.output.error("Track `{0}` could not be selected".format(track_name))
            return
        clip = self.parser.parse(clip_string, self.create_clip)
        track.add_clip(clip)

    def run(self, command: str, **kwargs):
        self.do_run(**kwargs)
