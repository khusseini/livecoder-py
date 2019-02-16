from livecoder.sequencer import Sequencer
from livecoder.player import Player
from livecoder import midi


class LiveCoder:
    def __init__(self, bpm: int = 110, fpb: int = 24):
        self.sequencer = Sequencer(bpm, fpb)
        self.player = Player(self.sequencer)

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

    def select_output(self, index: int):
        midi.select_output(index)
        return self.get_output()

    def select_input(self, index: int):
        midi.select_input(index)
        midi.get_selected_input().callback = self.on_message
        return self.get_input()

    def close(self):
        self.player.stop()
        i = 0
        for o in self.list_outputs():
            out = self.select_output(i)
            out.reset()
            i += 1

    @staticmethod
    def get_output():
        return midi.get_selected_output()

    @staticmethod
    def get_input():
        return midi.get_selected_input()

    def on_message(self, m):
        player = self.player

        if m.type == 'start':
            player.compile()
            player.start()
            return

        if m.type == 'stop':
            player.stop()
            self.get_output().reset()
            return

        if m.type == 'continue':
            player.compile()
            player.start()
            return

        if m.type == 'songpos':
            player.stop()
            player.compile()
            self.get_output().reset()
            return

        if m.type == 'clock':
            player.tick(self.on_send)
            return

    def on_send(self, msg):
        self.get_output().send(msg)
