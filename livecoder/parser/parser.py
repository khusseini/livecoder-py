import lark
from .transformer import Transformer
from livecoder.sequencer import Clip
from livecoder.sequencer.functions import FunctionRegistry

lark_definitions = r"""
    clip: "[" clip_length ":" BOOL WS* clip_step (WS* "," WS* clip_step)* "]"
    clip_length: INT
               | FRACTION
    clip_step: function|group
    function: CNAME "(" WS* func_arg (WS* "," WS* func_arg)* ")"
    func_arg: group|note_sequence
    group: GROUP_INDEX ":" WS* note_sequence
    note_sequence: [note_length (WS+ note_length)*]
    note_length: pause
               | FRACTION
    pause: "p" FRACTION
    FRACTION: SIGNED_INT "/" INT
            | INT "/" INT
        
    GROUP_INDEX: INT
               | NOTE
               | WORD
    BOOL: "0"
        | "1"
    
    NOTE: "a".."g" MOD? (INT|SIGNED_INT)?
        | "A".."G" MOD? (INT|SIGNED_INT)? 
        
    SYMBOL: DIGIT
          | LETTER
          | MOD
          | "-"
    
    MOD: "#"
       | "b"

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.SIGNED_INT
    %import common.DIGIT
    %import common.LETTER
    %import common.INT
    %import common.WORD
    %import common.CNAME
    %import common.WS
"""


class Parser:
    def __init__(self, start: str = 'clip'):
        self.lark = lark.Lark(lark_definitions, start=start)

    def parse(self, text_to_parse: str, registry: FunctionRegistry = None) -> Clip:
        transformer = Transformer(text_to_parse, registry)
        return transformer.transform(self.lark.parse(text_to_parse))
