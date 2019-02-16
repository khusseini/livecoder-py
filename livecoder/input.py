from urwid.widget import Edit


class Input:
    def __init__(self, widget: Edit):
        self.widget = widget

    def prompt(self, label: str):
        self.widget.set_edit_text('')
        self.widget.set_caption(label)

    def get(self):
        return self.widget.get_edit_text()

    def hide(self):
        self.prompt("")
