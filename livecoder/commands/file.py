from .command import Command


class SaveToFile(Command):
    def do_run(self, file_path: str):
        self.output.info("Command not implemented yet")

    def run(self, command: str, **kwargs):
        self.do_run(**kwargs)
