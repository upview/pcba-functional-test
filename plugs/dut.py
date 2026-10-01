"""DUT over the fixture UART (mock).

The production firmware exposes a test mode on a fixture-pulled GPIO: it
reports raw ADC readings, toggles GPIOs on command and enters stop mode.
Swap for a pyserial implementation; the phases stay unchanged.
"""

import numpy as np

from plugs import bench

ADC_FS_V = 3.3
ADC_BITS = 12


class DutSerial:
    def __init__(self):
        self._rng = np.random.default_rng()
        # Board-to-board ADC errors, within limits; the linearity phase measures them.
        self._gain = 1.0018 + self._rng.normal(0.0, 0.0008)
        self._offset_v = 0.0021 + self._rng.normal(0.0, 0.0008)
        print("DUT UART open at 115200")

    def enter_test_mode(self):
        return True

    def firmware_version(self):
        return "2.4.1"

    def hardware_revision(self):
        return "C"

    def set_gpio(self, channel, level):
        bench.write(f"gpio{channel}", level)

    def read_adc_volts(self):
        """ADC reading the firmware reports for the voltage on its input pin, in volts."""
        v = bench.read("stimulus_v", 0.0) * self._gain + self._offset_v + self._rng.normal(0.0, 0.0006)
        code = round(np.clip(v, 0.0, ADC_FS_V) / ADC_FS_V * (2**ADC_BITS - 1))
        return code / (2**ADC_BITS - 1) * ADC_FS_V

    def enter_stop_mode(self):
        return True
