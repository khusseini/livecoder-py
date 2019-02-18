import livecoder.application
import livecoder.commands

app = livecoder.application.Application({})


def run_quit(_cmd: livecoder.commands.Command, command: str, **kwargs):
    app.close()
    return command


def set_fpb(_cmd: livecoder.commands.Command, command: str, frames_per_beat: int, **kwargs):
    _cmd.app.livecoder.midi_player.set_timing(int(frames_per_beat))
    return command


def set_server(_cmd: livecoder.commands.Command, command: str, address: str):
    _cmd.app.livecoder.connect_server_port(address)
    return command


def run_help(_cmd: livecoder.commands.Command, command: str, **kwargs):
    app.output.info("Available Commands:")
    for regex in app.commands:
        app.output.info("{0}: {1}".format(regex, app.commands[regex]["description"]))
        if "examples" in app.commands[regex]:
            app.output.list(app.commands[regex]["examples"], "Examples:", False)
    app.output.info("")


app.commands = {
    "(?P<command>d(?:ev)?)(?: (?P<type>i(?:nput)?|o(?:tput)?) (?P<index>\\d+))?": {
        "cmd": livecoder.commands.SelectDeviceCommand(app, app.output),
        "description": "Select or list MIDI I/O"
    },
    "(?P<command>c(?:onnect)?) (?P<address>[^:]+:\\d+)": {
        "cmd": livecoder.commands.Command(app, app.output, set_server),
        "description": "Connect to TCP Server"
    },
    "(?P<command>t(?:rack)?)(?: (?P<track_name>\\w+))?": {
        "cmd": livecoder.commands.CreateTrackCommand(app, app.output),
        "description": "Select, list or create tracks"
    },
    "(?P<command>fpb) (?P<frames_per_beat>\d+)": {
        "cmd": livecoder.commands.Command(app, app.output, set_fpb),
        "description": "Set the frames per beat used in Sequencer"
    },
    "(?P<command>s(ave)?) (?P<file_path>.*)$": {
        "cmd": livecoder.commands.SaveToFile(app, app.output),
        "description": "Saves tracks to MIDI file"
    },
    "(?P<command>q(uit)?)": {
        "cmd": livecoder.commands.command.Command(app, app.output, run_quit),
        "description": "Quits Livecoder"
    },
    "(?P<command>h(elp)?)": {
        "cmd": livecoder.commands.command.Command(app, app.output, run_help),
        "description": "Displays Livecoder help"
    }
}

app.run()
