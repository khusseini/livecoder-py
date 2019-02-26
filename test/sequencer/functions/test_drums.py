import unittest
from livecoder.sequencer.functions import Drums
from livecoder.sequencer import Note


class TestParser(unittest.TestCase):
    def test_do_run(self):
        """"
        drums(k:1/4, sn: p1/2 1/2, hho: 1/8)
        """
        args = {"groups": {
            "k": [{"is_pause": False, "length": 1/4}],
            "sn": [{"is_pause": True, "length": 1/2}, {"is_pause": False, "length": 1/2}],
            "hho": [{"is_pause": False, "length": 1/8}]
        }}

        expected = {
            60: [Note(60, 1/4)],
            61: [Note(61, 1/8)],
            64: [Note(-1, 1/2), Note(64, 1/2)]
        }

        drums = Drums()
        actual = drums.do_run(**args)

        for num in expected:
            self.assertTrue(num in actual)

            actual_sequence = actual[num]
            expected_sequence = expected[num]

            set1 = set((x.number, x.length) for x in expected_sequence)
            diff = [x for x in actual_sequence if (x.number, x.length) not in set1]
            self.assertEqual(0, len(diff))
