#!/usr/bin/env python2.7
"""Run the pickle file generated by `align.py` or `bag_to_itoms.py`.

__date__ = 2019-02-28
__author__ = Denise Ratasich

"""

import argparse
import pickle

from model.itom import Itom, Itoms
from model.monitor import Monitor as SHSAMonitor


class Emulator(object):
    """Emulates monitor_node.py"""

    def __init__(self):
        self.__monitor = SHSAMonitor("../config/dmin.pl", 'dmin',
                                     librarypaths=["/python_ws/shsa-prolog/model"])
        self.__monitor.set_debug_callback(self.__debug_callback)

    @property
    def monitor(self):
        """Returns the monitor."""
        return self.__monitor

    def collect_inputs(self, data, period):
        """Collects itoms for monitor steps with given period (in seconds).

        Simulates the reception of itoms.

        """
        # itoms: [(t_reception, itom),..]
        itoms = sorted(data['itoms'], key=lambda msg: msg[0])
        signals = data['signals']
        # collect an itom of each signal for every monitor step
        inputs = []
        port = Itoms()
        t_last = itoms[0][0]  # t_reception of first itom
        for n, (t_cur, itom) in enumerate(itoms):
            # read itom into port
            port[itom.name] = itom
            # be sure to have received an itom of every signal
            if set(port.keys()) != set(signals):
                continue
            # ready to execute monitor for the first time
            if t_cur > t_last + period*1e9:
                inputs.append(Itoms(port))
                t_last = t_cur  # current time stamp
        print "number of steps: {}".format(len(inputs))
        return inputs

    def __validate(self, (outputs, values, error, failed)):
        assert self.__debug is not None
        # TODO check reproducability (output is the same like in the ROS run)
        assert self.__debug['failed'] == failed
        # reset debug callback
        self.__debug = None

    def __debug_callback(self, inputs, outputs, values, error, failed):
        self.__debug = {
            'inputs': inputs,
            'outputs': outputs,
            'values': list(values),
            'error': error,
            'failed': failed,
        }

    def __step(self, itoms):
        """Execute a monitor step."""
        failed = self.__monitor.monitor(itoms)
        failed = self.__monitor.substitutions.index(failed)
        return self.__debug['outputs'], self.__debug['values'], \
            self.__debug['error'], failed

    def run(self, data):
        inputs = data['inputs']
        manipulated = True
        # in case align generated the data we have sth to compare to
        try:
            self.__manipulated = data['manipulated']
            exp_outputs = data['outputs']
            assert len(inputs) == len(outputs)
        except Exception as e:
            pass
        # run monitor for each Itoms in inputs
        act_outputs = []
        for n in range(len(inputs)):
            # execute monitor
            output = self.__step(inputs[n])
            act_outputs.append(output)
            # check
            if not manipulated:
                self.__validate(exp_outputs[n])
        return act_outputs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Run monitor with given sequence of itoms.""")
    parser.add_argument("picklefile", type=str,
                        help="""Data (pickle file) containing sequence of itoms.""")
    args = parser.parse_args()

    with open(args.picklefile, 'rb') as f:
        data = pickle.load(f)

    emulator = Emulator()
    data['inputs'] = emulator.collect_inputs(data, 0.1)
    data['outputs'] = emulator.run(data)
    data['substitutions'] = emulator.monitor.substitutions

    with open(args.picklefile, 'wb') as f:
        pickle.dump(data, f, protocol=-1)