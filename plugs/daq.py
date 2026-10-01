"""Fixture DAQ (mock NI cDAQ-class): rail sense, GPIO loopback, AWG stimulus, photodiode."""

import numpy as np

RAILS = {"3v3": 3.30, "5v": 5.00, "1v8": 1.80}
GPIO_CHANNELS = 32


class FixtureDaq:
    def __init__(self):
        self._rng = np.random.default_rng(7)
        self._stimulus_v = 0.0
        print("Fixture DAQ ready: 32 DIO, 8 AI, 1 AO")

    def measure_rail(self, name):
        return RAILS[name] * (1.0 + self._rng.normal(0.0, 0.004))

    def measure_ripple_mv(self, name):
        return {"3v3": 12.0, "5v": 18.0, "1v8": 9.0}[name] + self._rng.normal(0.0, 1.0)

    def read_gpio(self, channel):
        """Level seen on the fixture side of loopback channel `channel`."""
        return self._driven.get(channel, 0)

    def drive_gpio_from_dut(self, channel, level):
        # Mock: the DUT drives, the fixture reads the same line through the loopback jumper.
        if not hasattr(self, "_driven"):
            self._driven = {}
        self._driven[channel] = level

    def set_stimulus(self, volts):
        self._stimulus_v = float(volts)

    def stimulus(self):
        return self._stimulus_v

    def photodiode_mv(self, led):
        return {"status_green": 412.0, "fault_red": 3.0}[led] + self._rng.normal(0.0, 4.0)
