import lark
from .transformer import Transformer

lark_definitions = r"""
    clip: "[" INT ":" BOOL WS* clip_step (WS+ clip_step)* "]"
    clip_step: function
    function: CNAME "(" WS* func_arg ("," WS* func_arg)* ")"
    func_arg: group|note_sequence
    group: GROUP_INDEX ":" WS* note_sequence
    note_sequence: [note_length (WS+ note_length)*]
    note_length: pause
               | fraction
    pause: "p" fraction
    fraction: SIGNED_INT "/" INT
            | INT "/" INT
            
    GROUP_INDEX: INT
               | WORD
    BOOL: "0"
        | "1"

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.SIGNED_INT
    %import common.INT
    %import common.WORD
    %import common.CNAME
    %import common.WS
"""


class Parser:
    def __init__(self):
        self.lark = lark.Lark(lark_definitions, start='clip')

    def parse(self, text_to_parse: str, factory_method: callable):
        transformer = Transformer(factory_method)
        return transformer.transform(self.lark.parse(text_to_parse))
