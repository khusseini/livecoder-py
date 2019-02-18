from .function import Function


class FunctionRegistry:
    functions: dict = {}

    def __init__(self, functions: list = ()):
        for f in functions:
            self.add_function(f)

    def add_function(self, func: Function):
        self.functions[func.name] = func

    def get_function(self, name: str):
        if name in self.functions:
            return self.functions[name]
        raise ValueError("Function `{}` does not exist".format(name))

    def call(self, name: str, **kwargs):
        return self.get_function(name).run(**kwargs)


