"""Fixture DAQ (mock NI cDAQ-class): interlocks, rail sense, GPIO loopback, AWG stimulus, photodiodes.

Swap for an nidaqmx implementation; the phases stay unchanged.
"""

import numpy as np

from plugs import bench

GPIO_CHANNELS = 32
RAILS_V = {"3v3": 3.30, "5v": 5.00, "1v8": 1.80}
RIPPLE_MVPP = {"3v3": 12.0, "5v": 18.0, "1v8": 9.0}
PHOTODIODE_MV = {"status_green": 412.0, "fault_red": 3.0}


class FixtureDaq:
    def __init__(self):
        self._rng = np.random.default_rng()
        print("Fixture DAQ ready: 32 DIO, 8 AI, 1 AO")

    def lid_closed(self):
        return True

    def vacuum_kpa(self):
        return -62.0 + self._rng.normal(0.0, 1.5)

    def measure_rail(self, name):
        return RAILS_V[name] * (1.0 + self._rng.normal(0.0, 0.004))

    def measure_ripple_mvpp(self, name):
        return RIPPLE_MVPP[name] + self._rng.normal(0.0, 1.0)

    def read_gpio(self, channel):
        """Level seen on the fixture side of loopback channel `channel`."""
        return bench.read(f"gpio{channel}", 0)

    def set_stimulus(self, volts):
        """Drive the analog output wired to the DUT ADC input."""
        bench.write("stimulus_v", float(volts))

    def photodiode_mv(self, led):
        return PHOTODIODE_MV[led] + self._rng.normal(0.0, 4.0)
