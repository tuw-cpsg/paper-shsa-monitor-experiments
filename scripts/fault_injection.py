#!/usr/bin/env python2.7
"""Manipulate the pickle file generated by `bag_to_itoms.py`.

__date__ = 2019-02-28
__author__ = Denise Ratasich

"""

import argparse
import pickle

from model.itom import Itom, Itoms
from model.monitor import Monitor as SHSAMonitor


class FaultInjection(object):
    """Manipulates a list of itoms."""

    def __init__(self):
        self.__manipulated = False

    @property
    def manipulated(self):
        return self.__manipulated

    def time_shift(self, itoms, signal, dt):
        """Shifts the reception of the itoms of the given signal by dt.

        itoms -- dictionary of itoms with key = reception time stamp
        dt -- time in seconds to shift the itoms
        """
        pass
        self.__manipulated = True

    def add_random_noise(self, itoms, signal, snr):
        pass
        self.__manipulated = True

    def stuck_to_zero(self, itoms, signal, t_from, t_to):
        pass
        self.__manipulated = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Manipulate itoms of given signal.""")
    parser.add_argument("picklefile", type=str,
                        help="""Data (pickle file) containing itoms.""")
    parser.add_argument("signal", type=str,
                        help="Signal to manipulate.")
    parser.add_argument("-t", "--timeshift", type=float, default=0,
                        help="Shift itoms by TIMESHIFT seconds.")
    parser.add_argument("-n", "--noise", type=float, default=0,
                        help="Add random noise, uniformly distributed from [0,NOISE].")
    parser.add_argument("-s", "--stuck-at", metavar=("FROM", "TO"), type=float, nargs=2,
                        help="Stuck to 0 between FROM and TO.")
    args = parser.parse_args()

    with open(args.picklefile, 'rb') as f:
        data = pickle.load(f)

    fi = FaultInjection()

    itoms = data['itoms']
    if args.timeshift > 0:
        itoms = fi.time_shift(args.time_shift)
    if args.noise > 0:
        itoms = fi.add_random_noise(itoms, args.signal, args.noise)
    if args.stuck_at is not None:
        itoms = fi.stuck_at(itoms, args.signal, args.stuck_at[0], args.stuck_at[1])

    data['itoms'] = itoms
    data['manipulated'] = fi.manipulated

    with open(args.picklefile, 'wb') as f:
        pickle.dump(data, f, protocol=-1)