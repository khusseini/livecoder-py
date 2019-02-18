from livecoder.output import Output
from livecoder.input import Input
from livecoder import LiveCoder
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
    cmd_mode: bool = False
    livecoder: LiveCoder
    output: Output
    command: dict

    def __init__(self, commands: dict):
        self.commands = commands
        self.livecoder = LiveCoder()
        self.output = Output()

        palette = [
            ('title', 'white', 'default', 'bold'),
            ('info', 'yellow', 'default'),
            ('error', 'dark red', 'default')
        ]

        commander = urwid.Edit('', multiline=False)
        frame = Window(self.output.widget, commander, self.on_window_keypress)
        loop = urwid.MainLoop(frame, palette=palette)

        self.loop = loop
        self.input = Input(commander)
        self.input_buffer = ''

    def run(self):
        self.loop.run()

    def close(self):
        self.livecoder.close()
        self.loop.screen.clear()
        raise urwid.ExitMainLoop

    def process_command(self, cmd: str):
        self.output.info('--> Received command: ' + repr(cmd))
        for c in self.commands:
            command = self.commands[c]["cmd"]
            test = re.compile(c)
            matches = test.match(cmd)
            if matches:
                result = command.run(**matches.groupdict())
                if result is not None:
                    cmd = result

    def on_window_keypress(self, key, size):
        if key == 'esc':
            self.input.hide()
            self.cmd_mode = False
            return

        if key == 'enter' and self.cmd_mode:
            self.process_command(self.input_buffer)
            self.input_buffer = ''
            self.input.hide()
            self.cmd_mode = False
            return

        if self.cmd_mode:
            if key == 'backspace':
                self.input_buffer = self.input_buffer[:-1]
            else:
                self.input_buffer += key
            self.input.widget.set_edit_text(self.input_buffer)
            return

        if key == ':' and not self.cmd_mode:
            self.output.info('--> Command mode activated')
            self.input.prompt(": ")
            self.input.widget.set_edit_text(self.input_buffer)
            self.cmd_mode = True
            return

