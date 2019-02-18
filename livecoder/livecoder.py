import livecoder.midi as midi
from livecoder.sequencer import MidiPlayer


class LiveCoder:
    midi_player: MidiPlayer

    def __init__(self):
        self.server_port = None
        self.server_port_address = ""
        self.midi_player = MidiPlayer()

    @staticmethod
    def get_input_index():
        return midi.midi_opts["i_index"]

    @staticmethod
    def get_output_index():
        return midi.midi_opts["o_index"]

    @staticmethod
    def list_inputs():
        return midi.midi_opts["input_names"]

    @staticmethod
    def list_outputs():
        return midi.midi_opts["output_names"]

    @staticmethod
    def get_output():
        return midi.get_selected_output()

    @staticmethod
    def get_input():
        return midi.get_selected_input()

    def select_output(self, index: int):
        midi.select_output(index)
        self.midi_player.set_output(self.get_output())
        return self.get_output()

    def connect_server_port(self, address: str):
        self.server_port_address = address
        self.midi_player.output = self.server_port
        if address == "-":
            if self.server_port:
                self.server_port.reset()
                self.server_port.close()
                self.server_port = None
            return

        self.server_port = midi.connect(address)

    def select_input(self, index: int):
        midi.select_input(index)
        midi.get_selected_input().callback = self.on_message
        return self.get_input()

    def close(self):
        if self.midi_player:
            self.midi_player.stop()
        if self.server_port:
            self.server_port.reset()
            self.server_port.close()
            return
        i = 0
        for o in self.list_outputs():
            out = self.select_output(i)
            out.reset()
            i += 1

    def start(self):
        if self.midi_player:
            self.midi_player.play()

    def stop(self):
        self.get_output().reset()
        if self.midi_player:
            self.midi_player.stop()

    def tick(self):
        if self.midi_player:
            self.midi_player.tick()

    def on_message(self, m):
        if m.type == 'start':
            self.start()
            return

        if m.type == 'stop':
            self.stop()
            return

        if m.type == 'continue':
            self.start()
            return

        if m.type == 'songpos':
            self.stop()
            return

        if m.type == 'clock':
            self.tick()
            return

