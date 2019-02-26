import unittest
from livecoder.sequencer.functions import Chords
from livecoder.sequencer import Note


class TestParser(unittest.TestCase):
    def test_do_run(self):
        """"
        i(0:p1/2 1/2, 1/4)
        """
        args = {
            "called_name": "i",
            "groups": {
                "0": [{"is_pause": True, "length": 1/2}, {"is_pause": False, "length": 1/2}],
                "_": [{"is_pause": False, "length": 1/4}]
            }
        }

        expected = {
            60: [Note(-1, 1/2), Note(60, 1/2)],
            64: [Note(64, 1/4)],
            67: [Note(67, 1/4)]
        }

        chords = Chords()
        actual = chords.do_run(**args)

        for num in expected:
            self.assertTrue(num in actual)

            actual_sequence = actual[num]
            expected_sequence = expected[num]

            set1 = set((x.number, x.length) for x in expected_sequence)
            diff = [x for x in actual_sequence if (x.number, x.length) not in set1]
            self.assertEqual(0, len(diff))
