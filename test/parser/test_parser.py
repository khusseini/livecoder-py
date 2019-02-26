import unittest
from livecoder.parser.parser import Parser
from livecoder.sequencer import Note
import livecoder.sequencer.functions as func


class TestParser(unittest.TestCase):
    def test_parse_clip(self):
        input = "[1:1 C3:1/4 p1/8 1/8, C#3:p1/8 1/8 1/4]"
        parser = Parser()

        p8 = Note(-1, 1/8)
        n604 = Note(60, 1/4)
        n608 = Note(60, 1/8)
        n614 = Note(61, 1/4)
        n618 = Note(61, 1/8)

        fpb = 400
        signature = 1/4
        factor = fpb * 1/signature
        eighth = int(1/8 * factor)
        fourth = int(1/4 * factor)
        dotted_fourth = int(3/8 * factor)

        expected = (
            (0, [n604, p8]),
            (eighth, [n618]),
            (fourth, [p8, n614]),
            (dotted_fourth, [n608])
        )

        clip = parser.parse(input)
        frames = clip.compile(fpb, signature)
        self.assertEqual(factor*1/2, len(frames))

        for e in expected:
            set1 = set((x.number, x.length) for x in e[1])
            diff = [x for x in frames[e[0]] if (x.number, x.length) not in set1]
            self.assertEqual(0, len(diff))

    def test_parse_function(self):
        parser = Parser('function')

        registry = func.FunctionRegistry([
            func.Drums(),
            func.Chords()
        ])

        self.run_drums(parser, registry)
        self.run_chords(parser, registry)

    def run_chords(self, parser, registry):
        input = "i(0:p1/2 1/2, 1/4)"
        func_info = parser.parse(input, registry)
        actual = registry.call(func_info["name"], **func_info["args"])
        expected = {
            60: [Note(-1, 1/2), Note(60, 1/2)],
            64: [Note(64, 1/4)],
            67: [Note(67, 1/4)]
        }
        for num in expected:
            self.assertTrue(num in actual)

            actual_sequence = actual[num]
            expected_sequence = expected[num]

            set1 = set((x.number, x.length) for x in expected_sequence)
            diff = [x for x in actual_sequence if (x.number, x.length) not in set1]
            self.assertEqual(0, len(diff))

    def run_drums(self, parser, registry):
        input = "drums(k:1/4, sn: p1/2 1/2, hho: 1/8)"
        func_info = parser.parse(input, registry)
        actual = registry.call(func_info["name"], **func_info["args"])
        expected = {
            60: [Note(60, 1/4)],
            61: [Note(61, 1/8)],
            64: [Note(-1, 1/2), Note(64, 1/2)]
        }
        for num in expected:
            self.assertTrue(num in actual)

            actual_sequence = actual[num]
            expected_sequence = expected[num]

            set1 = set((x.number, x.length) for x in expected_sequence)
            diff = [x for x in actual_sequence if (x.number, x.length) not in set1]
            self.assertEqual(0, len(diff))
