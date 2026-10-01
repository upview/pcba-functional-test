"""DUT over the fixture UART (mock).

The production firmware exposes a test mode on a fixture-pulled GPIO: it
reports raw ADC readings, toggles GPIOs on command and enters stop mode.
"""

import numpy as np

ADC_FS_V = 3.3
ADC_BITS = 12


class DutSerial:
    def __init__(self):
        self._rng = np.random.default_rng(3)
        self._test_mode = False
        self._gain = 1.0018   # ADC gain error the linearity phase must catch
        self._offset_v = 0.0021
        print("DUT UART open at 115200")

    def enter_test_mode(self):
        self._test_mode = True
        return True

    def firmware_version(self):
        return "2.4.1"

    def hardware_revision(self):
        return "C"

    def set_gpio(self, channel, level):
        return True

    def read_adc(self, stimulus_v):
        """ADC code the firmware reports for the given fixture stimulus."""
        v = float(stimulus_v) * self._gain + self._offset_v + self._rng.normal(0.0, 0.0006)
        code = int(round(np.clip(v, 0.0, ADC_FS_V) / ADC_FS_V * (2**ADC_BITS - 1)))
        return code

    def enter_stop_mode(self):
        return True
