from livecoder.application import Application
from livecoder import command
from livecoder.livecoder import LiveCoder

app = Application([])


def run_quit(text, *args):
    app.close()
    return text


def set_fpb(text, livecoder: LiveCoder):
    fpb = text.split(' ')[1]
    livecoder.sequencer.fpb = fpb
    return text


app.commands = [
    command.Command('q(uit)?', app.output, run_quit),
    command.SaveToFile('s(ave)?', app.output),
    command.SelectDeviceCommand('d(?:ev)?', app.output),
    command.CreateTrackCommand('t(?:rack)?', app.output),
    command.Command('fpb', app.output, set_fpb),
    command.ParseSequenceCommand(app.output)
]

app.run()
