import mido
from livecoder.note import Note


midi_opts = {
    'i_index': 0,
    'o_index': 0,
    'output_names': mido.get_output_names(),
    'input_names': mido.get_input_names(),
    'outputs': {},
    'inputs': {}
}


def get_selected_output():
    if midi_opts["o_index"] in midi_opts["outputs"]:
        return midi_opts["outputs"][midi_opts["o_index"]]
    return None


def get_selected_input():
    if midi_opts["i_index"] in midi_opts["inputs"]:
        return midi_opts["inputs"][midi_opts["i_index"]]
    return None


def select_output(index: int):
    if index > len(midi_opts["output_names"]) - 1 or index < 0:
        return False
    midi_opts["o_index"] = index
    if midi_opts["o_index"] not in midi_opts["outputs"]:
        midi_opts["outputs"][midi_opts["o_index"]] = mido.open_output(midi_opts["output_names"][index])


def select_input(index: int):
    if index > len(midi_opts["output_names"]) or index < 0:
        return False
    midi_opts["i_index"] = index
    if midi_opts["i_index"] not in midi_opts["inputs"]:
        midi_opts["inputs"][midi_opts["i_index"]] = mido.open_input(midi_opts["input_names"][index])
    return True


def note_message(action: str, n: Note, ch: int = 0, time: int = 0):
    return create_message(action, note=n.number, channel=ch, velocity=n.velocity, time=time)


def create_message(message_type: str, **kwargs):
    return mido.Message(message_type, **kwargs)
