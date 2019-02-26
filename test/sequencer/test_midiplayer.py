import unittest
from livecoder.sequencer.track import Track
from livecoder.sequencer.clip import Clip
from livecoder.sequencer.note import Note
from livecoder.sequencer.midiplayer import MidiPlayer
import livecoder.sequencer.functions as func
import mido


class TestTrack(unittest.TestCase):
    def test_get_frame(self):
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
        track.add_clip(clip)
        player = MidiPlayer()
        player.add_track(track)

        fpb = 400
        signature = 1/4
        factor = fpb * 1/signature
        eighth = int(1/8 * factor)
        fourth = int(1/4 * factor)
        dotted_fourth = int(3/8 * factor)

        m604 = mido.Message(
            'note_on',
            note=n604.number,
            velocity=n604.velocity,
            time=player.length_to_ticks(n604.length),
            channel=0
        )
        mo604 = mido.Message(
            'note_off',
            note=n604.number,
            channel=0
        )
        m608 = mido.Message(
            'note_on',
            note=n608.number,
            velocity=n608.velocity,
            time=player.length_to_ticks(n608.length),
            channel=0
        )
        mo608 = mido.Message(
            'note_off',
            note=n608.number,
            channel=0
        )

        m618 = mido.Message(
            'note_on',
            note=n618.number,
            velocity=n618.velocity,
            time=player.length_to_ticks(n618.length),
            channel=0
        )
        mo618 = mido.Message(
            'note_off',
            note=n618.number,
            channel=0
        )
        m614 = mido.Message(
            'note_on',
            note=n614.number,
            velocity=n614.velocity,
            time=player.length_to_ticks(n614.length),
            channel=0
        )
        mo614 = mido.Message(
            'note_off',
            note=n614.number,
            channel=0
        )

        expected_length = int(factor * 1/2)
        expected = {
            0: [m604],
            eighth: [m618],
            fourth-1: [mo604, mo618],
            fourth: [m614],
            fourth + eighth: [m608],
            (fourth+fourth)-1: [mo614, mo608]
        }

        player.play()
        for i in range(0, expected_length):
            messages = player.get_frame()
            if i in expected:
                self.assertEqual(expected[i], messages, "Frame mismatch at {0}".format(i))
