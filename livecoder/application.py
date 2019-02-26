from livecoder.output import Output
from livecoder.input import Input
from livecoder import LiveCoder
from livecoder.state import State
import livecoder.sequencer.functions as func
import re
import urwid


class Window(urwid.Frame):
    def __init__(self, body, footer, on_key):
        super(Window, self).__init__(body, footer=footer)
        self.on_key = on_key

    def keypress(self, size, key):
        key = super(Window, self).keypress(size, key)
        self.on_key(key, size)
        return key


class Application:
    _clip_functions: func.FunctionRegistry
    _cmd_mode: bool = False
    _commands: dict
    _input: Input
    _input_buffer: str
    _livecoder: LiveCoder
    _loop: urwid.MainLoop
    _output: Output
    _state: State

    @property
    def commands(self):
        return self._commands

    @commands.setter
    def commands(self, value: dict):
        self._commands = value

    @property
    def clip_functions(self):
        return self._clip_functions

    @property
    def state(self):
        return self._state

    @property
    def output(self):
        return self._output

    @property
    def livecoder(self):
        return self._livecoder

    def __init__(self, clip_functions: func.FunctionRegistry, commands: dict = {}):
        self._commands = commands
        self._livecoder = LiveCoder()
        self._livecoder.midi_player.frames_per_beat = 24
        self._output = Output()
        self._state = State()
        self._clip_functions = clip_functions

        palette = [
            ('title', 'white', 'default', 'bold'),
            ('info', 'yellow', 'default'),
            ('error', 'dark red', 'default')
        ]

        commander = urwid.Edit('', multiline=False)
        frame = Window(self._output.widget, commander, self.on_window_keypress)
        loop = urwid.MainLoop(frame, palette=palette)

        self._loop = loop
        self._input = Input(commander)
        self._input_buffer = ''

    def run(self):
        self._loop.run()

    def close(self):
        self._livecoder.close()
        self._loop.screen.clear()
        raise urwid.ExitMainLoop

    def process_command(self, cmd: str):
        cmd = cmd.strip()
        self._output.info('--> Received command: ' + repr(cmd))
        for c in self._commands:
            command = self._commands[c]["cmd"]
            test = re.compile(c)
            matches = test.match(cmd)
            if matches:
                result = command.run(**matches.groupdict())
                if result is None:
                    break
                cmd = result

    def on_window_keypress(self, key, size):
        if key == 'esc':
            self._input.hide()
            self._cmd_mode = False
            return

        if key == 'enter' and self._cmd_mode:
            self.process_command(self._input_buffer)
            self._input_buffer = ''
            self._input.hide()
            self._cmd_mode = False
            return

        if self._cmd_mode:
            if key == 'backspace':
                self._input_buffer = self._input_buffer[:-1]
            elif len(key) == 1:
                self._input_buffer += key
            self._input.widget.set_edit_text(self._input_buffer)
            return

        if key == ':' and not self._cmd_mode:
            self._output.info('--> Command mode activated')
            self._input.prompt(": ")
            self._input.widget.set_edit_text(self._input_buffer)
            self._cmd_mode = True
            return
