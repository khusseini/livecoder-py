import re
from livecoder.livecoder import LiveCoder
from livecoder.output import Output
from livecoder import note
from livecoder import chord


class Command:
    def __init__(self, name: str, output: Output, run_command: callable = None):
        self.name = name
        self.regex = Command.cmd_regex(name)
        self.output = output
        self.run_command = run_command

    def supports(self, text: str):
        return self.regex.match(text)

    def run(self, text: str,  livecoder: LiveCoder):
        if self.run_command:
            return self.run_command(text, livecoder)
        return text

    @staticmethod
    def func_regex(name: str):
        return re.compile(name + " (.+)")

    @staticmethod
    def cmd_regex(name: str):
        return re.compile(name)

    @staticmethod
    def select_regex(name: str):
        return re.compile(name + "(?: (.+))?")


class SelectDeviceCommand(Command):
    def __init__(self, name:str, output: Output):
        Command.__init__(self, name, output)
        self.regex = Command.select_regex(self.name)
        self.livecoder = None

    def mark_input_device(self, index, device):
        return index == self.livecoder.get_input_index()

    def mark_output_device(self, index, device):
        return index == self.livecoder.get_output_index()

    def run(self, text: str,  livecoder: LiveCoder):
        self.livecoder = livecoder
        matches = self.regex.match(text)
        if matches.group(1):
            match = matches.group(1).split(' ')
            io = match[0]
            num = int(match[1])
            if io == 'i':
                livecoder.select_input(num)
                self.output.info('Selected Input {}'.format(livecoder.list_inputs()[num]))
            elif io == 'o':
                livecoder.select_output(num)
                self.output.info('Selected Output {}'.format(livecoder.list_outputs()[num]))
            else:
                self.output.error('First argument of dev has to be either `i` or `o`.')
        else:
            self.output.list(livecoder.list_outputs(), 'Outputs available: ', True, self.mark_output_device)
            self.output.list(livecoder.list_inputs(), 'Inputs available: ', True, self.mark_input_device)
            self.output.info('Use with dev(i|o \\d+)')

        return text


class CreateTrackCommand(Command):
    def __init__(self, name: str, output: Output):
        Command.__init__(self, name, output)
        self.regex = Command.select_regex(self.name)
        self.livecoder = None

    def run(self, text: str, livecoder: LiveCoder):
        self.livecoder = livecoder
        matches = self.regex.match(text)
        if matches.group(1):
            match = matches.group(1).split(' ')

            if match[0] == 'sel':
                if len(match) != 2:
                    raise ValueError("`track sel <name>` wrong parameter count")
                livecoder.sequencer.select_track(match[1])
                return

            for track_name in match:
                self.output.info('Creating track {}'.format(track_name))
                livecoder.sequencer.create_track(track_name, len(livecoder.sequencer.tracks))
        else:
            tracks = []
            for t in livecoder.sequencer.tracks:
                tracks.append(t)
            self.output.list(tracks, 'Current tracks', False, self.mark_track)

    def mark_track(self, index, item):
        return item == self.livecoder.sequencer.selected_track_name


class ParseSequenceCommand(Command):
    def __init__(self, output: Output):
        super(ParseSequenceCommand, self).__init__('([^@]*@\\d+/\\d+)( +[^@]*@\\d+/\\d+)*', output)
        self.parse_regex = re.compile('([^@]*)?@(\\d+/\\d+)')
        self.note_regex = re.compile('[A-G]')
        self.interval_regex = chord.interval_regex

    def run(self, text: str,  livecoder: LiveCoder):
        steps = text.split(' ')
        for step in steps:
            step_matches = self.parse_regex.match(step)
            if not step_matches:
                self.output.error('Step `{}` did not validate'.format(step))
                continue

            note_or_interval = step_matches.group(1)
            note_length = eval(step_matches.group(2))
            notes = []

            if note.note_regex.match(note_or_interval):
                note_to_play = note.from_string(note_or_interval)
                notes.append(note_to_play)

            if self.interval_regex.match(note_or_interval):
                notes = chord.Chord(note_or_interval).get_notes(note.Note(60))

            livecoder.sequencer.selected_track().append_notes(note_length, notes)

        ticks = livecoder.sequencer.compile_tick_list()
        self.output.info(repr(ticks))
        self.output.info('Added {0} to track {1} (Ch {2})'.format(
            text,
            livecoder.sequencer.selected_track_name,
            livecoder.sequencer.selected_track().channel
        ))


class SaveToFile(Command):
    def __init__(self, name: str, output:Output):
        super(SaveToFile, self).__init__(name, output)
        self.regex = Command.func_regex(name)

    def run(self, text: str,  livecoder: LiveCoder):
        mf = livecoder.sequencer.export_file()
        mf.save(format(text.split(' ')[1]))
