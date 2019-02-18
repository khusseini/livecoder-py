from livecoder.output import Output
from livecoder.application import Application


class Command:
    output: Output
    run_command: callable
    app: Application

    def __init__(self, app: Application, output: Output, run_command: callable = None):
        self.output = output
        self._run_command = run_command
        self.app = app

    def run(self, command: str, **kwargs):
        if self._run_command:
            return self._run_command(self, command, **kwargs)
        return
