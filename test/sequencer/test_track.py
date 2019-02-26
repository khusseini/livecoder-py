import unittest
from livecoder.sequencer.track import Track
from livecoder.sequencer.clip import Clip
from livecoder.sequencer.note import Note
import livecoder.sequencer.functions as func


class TestTrack(unittest.TestCase):
    def test_dirty_state(self):
        """
        Test that it sets itself dirty when changing the state
        """
        track = Track("test", 0)
        self.assertTrue(track.is_dirty)

        track.compile()
        self.assertFalse(track.is_dirty)

        clip = Clip("test", func.FunctionRegistry([]))
        track.add_clip(clip)
        self.assertTrue(track.is_dirty)
        track.compile()
        self.assertFalse(track.is_dirty)

    def test_compile(self):
        track = Track("test", 0)
        p8 = Note(-1, 1/8)
        n604 = Note(60, 1/4)
        n608 = Note(60, 1/8)
        n614 = Note(61, 1/4)
        n618 = Note(61, 1/8)

        clip = Clip("", func.FunctionRegistry([]))
        # [1:1 C:1/4,p1/8,1/8 C#:p1/8 1/8 1/4]
        clip.add_sequence(n604, [n604, p8, n608])
        clip.add_sequence(n614, [p8, n618, n614])

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

        track.add_clip(clip)
        frames = track.compile(fpb, signature)

        self.assertEqual(factor*1/2, len(frames))
        for e in expected:
            self.assertEqual(e[1], frames[e[0]])

