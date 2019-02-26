from .command import Command


class SelectDeviceCommand(Command):
    def do_run(self, type: str = "", index: int = ""):
        if not type:
            return self.list()
        self.select(type, index)

    def run(self, command: str, **kwargs):
        self.do_run(**kwargs)

    def mark_input_device(self, index, device):
        return index == self.app._livecoder.get_input_index()

    def mark_output_device(self, index, device):
        return index == self.app._livecoder.get_output_index()

    def select(self, type: str, index: int):
        index = int(index)
        if type == 'i':
            self.app._livecoder.select_input(index)
            self.output.info('Selected Input {}'.format(self.app._livecoder.list_inputs()[index]))
            return
        if type == 'o':
            self.app._livecoder.select_output(index)
            self.output.info('Selected Output {}'.format(self.app._livecoder.list_outputs()[index]))
            return
        self.output.error('First argument of dev has to be either `i` or `o`.')

    def list(self):
        self.output.list(self.app._livecoder.list_outputs(), 'Outputs available: ', True, self.mark_output_device)
        self.output.list(self.app._livecoder.list_inputs(), 'Inputs available: ', True, self.mark_input_device)
        self.output.info('Use with dev(i|o \\d+)')


