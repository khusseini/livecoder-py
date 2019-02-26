from .sequencer_function import SequencerFunction


class FunctionRegistry:

    def __init__(self, functions: list = []):
        self._functions: list = functions

    def add_function(self, func: SequencerFunction):
        self._functions.append(func)

    def get_function(self, name: str):
        for f in self._functions:
            if f.matches_name(name):
                return f
        raise ValueError("Function `{}` does not exist".format(name))

    def has_function(self, name: str):
        for f in self._functions:
            if f.matches_name(name):
                return True
        return False

    def call(self, name: str, **kwargs):
        func = self.get_function(name)
        return func.run(called_name=name, **kwargs)
