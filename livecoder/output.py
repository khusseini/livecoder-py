import urwid


class Output:
    def __init__(self):
        self.body = urwid.SimpleFocusListWalker([])
        self.widget = urwid.ListBox(self.body)

    def info(self, text: str):
        self.widget.body.append(urwid.Text(('info', text)))
        if len(self.widget.body) > 1:
            self.widget.focus_position += 1

    def list(self, items: list, title: str = "", show_index: bool = True, mark_index:callable = None):
        self.info('')
        if len(title):
            self.info(title)
        index = 0
        for i in items:
            prev = ""
            post = ""
            if show_index:
                prev = str(index)+": "
            if mark_index and mark_index(index, i):
                post += " <--"
            self.info(prev+i+post)
            index += 1
        self.info('')

    def error(self, text: str):
        self.body.append(urwid.Text(('error', text)))

