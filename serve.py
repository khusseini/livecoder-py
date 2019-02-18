#!/usr/bin/env python
"""
Serve one or more output ports. Every message received on any of the
connected sockets will be sent to every output port.
"""
import argparse
import mido
from mido import sockets
from mido.ports import MultiPort
from livecoder.midi import midi_opts


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    arg = parser.add_argument

    arg('address',
        metavar='ADDRESS',
        help='host:port to serve on')

    arg('ports',
        metavar='PORT',
        nargs='+',
        help='output port to serve')

    return parser.parse_args()


args = parse_args()

try:
    i = 0
    for name in midi_opts["output_names"]:
        print("{0}: {1}".format(i, name))
        i += 1

    print("")

    out = MultiPort([mido.open_output(midi_opts["output_names"][int(index)]) for index in args.ports])
    (hostname, port) = sockets.parse_address(args.address)
    with sockets.PortServer(hostname, port) as server:
        for message in server:
            print('Received {}'.format(message))
            out.send(message)

except KeyboardInterrupt:
    pass
