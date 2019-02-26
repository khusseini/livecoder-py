class SequencerFunction:
    def __init__(self, name):
        self.name = name

    def run(self, **kwargs):
        print(self.name)

    def matches_name(self, name_to_match: str):
        if not isinstance(self.name, str):
            return self.name.match(name_to_match)

        return self.name == name_to_match
