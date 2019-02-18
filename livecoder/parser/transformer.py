import lark


class Transformer(lark.Transformer):
    def __init__(self, constructor: callable):
        super(Transformer, self).__init__()
        self._clip = constructor()

    def clip(self, items):
        self._clip.repeat = int(items.pop(0))
        self._clip.clip_fill = bool(items.pop(0))

        while len(items):
            i = items.pop(0)
            if isinstance(i, dict):
                self._clip.add(i)
        return self._clip

    def clip_step(self, items):
        return items[0]

    def function(self, items: list):
        func = {
            "name": str(items.pop(0)),
            "args": []
        }

        while len(items):
            i = items.pop(0)
            if isinstance(i, dict):
                func["args"].append(i)
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
            note["length"] = items[0].children[0]
        else:
            note["length"] = str(items[0])

        return note

    def fraction(self, items: list):
        return int(items[0]) / int(items[1])
