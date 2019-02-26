#!/usr/bin/env python

import livecoder.application
import livecoder.commands
import livecoder.sequencer.functions as func


def run_quit(_cmd: livecoder.commands.Command, command: str, **kwargs):
    app.close()
    return command


def set_fpb(_cmd: livecoder.commands.Command, command: str, frames_per_beat: int, **kwargs):
    _cmd.app.livecoder.midi_player.frames_per_beat = int(frames_per_beat)
    return command


def set_server(_cmd: livecoder.commands.Command, command: str, address: str):
    _cmd.app.livecoder.connect_server_port(address)
    return command


def run_help(_cmd: livecoder.commands.Command, command: str, **kwargs):
    app.output.info("Available Commands:")
    for regex in app.commands:
        app.output.info("{0}: {1}".format(regex, app.commands[regex].get("description", "")))
        if "examples" in app.commands[regex]:
            app.output.list(app.commands[regex]["examples"], "Examples:", False)
    app.output.info("")


app = livecoder.application.Application(func.FunctionRegistry([
    func.Drums(),
    func.Chords(),
]))

app.commands = {
    "^(?P<command>d(?:ev)?)(?: (?P<type>i(?:nput)?|o(?:tput)?) (?P<index>\\d+))?$": {
        "cmd": livecoder.commands.SelectDeviceCommand(app, app.output),
        "description": "Select or list MIDI I/O"
    },
    "^(?P<command>c(?:onnect)?) (?P<address>[^:]+:\\d+)$": {
        "cmd": livecoder.commands.Command(app, app.output, set_server),
        "description": "Connect to TCP Server"
    },
    "^(?P<command>t(?:rack)?)(?: (?P<track_name>\\w+))?$": {
        "cmd": livecoder.commands.CreateTrackCommand(app, app.output),
        "description": "Select, list or create tracks"
    },
    "^(?P<command>fpb) (?P<frames_per_beat>\\d+)$": {
        "cmd": livecoder.commands.Command(app, app.output, set_fpb),
        "description": "Set the frames per beat used in Sequencer"
    },
    "^(?P<command>s(ave)?) (?P<file_path>.*)$": {
        "cmd": livecoder.commands.SaveToFile(app, app.output),
        "description": "Saves tracks to MIDI file"
    },
    "^(?P<command>q(uit)?)$": {
        "cmd": livecoder.commands.Command(app, app.output, run_quit),
        "description": "Quits Livecoder"
    },
    "(?P<command>h(elp)?)": {
        "cmd": livecoder.commands.Command(app, app.output, run_help),
        "description": "Displays Livecoder help"
    },
    "(?P<command>(?P<track_name>\\w+) *(?P<clip_string>\\[.*\\]))": {
        "cmd": livecoder.commands.CreateClipCommand(app, app.output),
        "description": "Create a clip for a track",
        "examples": [
            "drums  [1:1 drums(k:1/4, sn:p1/2 1/2, hhc:1/16)]",
            "piano  [1:1 i(1/4) iii(0:p1/8 1/8, 1/4) ii(1/4) vi(1/4)]"
        ]
    }
}

app.run()
