import lark
from livecoder import sequencer
from livecoder.sequencer.functions import FunctionRegistry


class Transformer(lark.Transformer):
    def __init__(self, value: str, function_registry: FunctionRegistry = None):
        super(Transformer, self).__init__()
        self._clip = sequencer.Clip(value, function_registry)
        self._function_registry = function_registry

    @staticmethod
    def fill_note(num: int, from_dict: dict):
        note = sequencer.Note(num)
        note.length = from_dict["length"]
        if from_dict["is_pause"]:
            note.number = -1
        return note

    def function_exists(self, name: str):
        if self._function_registry is None:
            return False
        return self._function_registry.has_function(name)

    def clip(self, items):
        clip_length = float(eval(items.pop(0).children[0]))
        self._clip.clip_length = clip_length
        self._clip.clip_fill = bool(items.pop(0))

        while len(items):
            i = items.pop(0)
            if isinstance(i, dict):
                if "seq" in i:
                    n = sequencer.note.from_string(i["name"])
                    sequence = []
                    for s in i["seq"]:
                        note = self.fill_note(n.number, s)
                        sequence.append(note)
                    self._clip.add_sequence(n.number, sequence)
                elif "args" in i:
                    if not self.function_exists(i["name"]):
                        raise ValueError("Function {0} does not exist", i["name"])
                    self._clip.add_sequence(i["name"], i["args"])
        return self._clip

    def clip_step(self, items):
        return items[0]

    def function(self, items: list):
        func = {
            "name": str(items.pop(0)),
            "args": {
                "groups": {}
            }
        }

        while len(items):
            i = items.pop(0)
            if isinstance(i, dict):
                func["args"]["groups"][i["name"]] = i["seq"]
        return func

    def func_arg(self, items: list):
        while len(items):
            i = items.pop(0)
            if isinstance(i, dict):
                return i
            if isinstance(i, list):
                return {"name": "_", "seq": i}

    def group(self, items: list):
        group = {
            "name": str(items.pop(0)),
            "seq": []
        }
        while len(items):
            i = items.pop(0)
            if isinstance(i, list):
                group["seq"] = i
                break
        return group

    def note_sequence(self, items: list):
        seq = []
        for i in items:
            if isinstance(i, dict):
                seq.append(i)
        return seq

    def note_length(self, items: list):
        note = {
            "length": 0,
            "is_pause": False
        }

        if isinstance(items[0], lark.Tree):
            note["is_pause"] = items[0].data == 'pause'
            note["length"] = float(eval(items[0].children[0]))
        else:
            note["length"] = float(eval(items[0]))

        return note

    def fraction(self, items: list):
        return int(items[0]) / int(items[1])
