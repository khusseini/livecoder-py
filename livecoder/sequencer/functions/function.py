class Function:
    name: str

    def __init__(self, name: str, do_run: callable = None):
        self.name = name
        self._run = do_run

    def run(self, **kwargs):
        if self._run is not None:
            return self._run(**kwargs)
