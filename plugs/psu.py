"""Programmable DC supply on the fixture Vin rail (mock Rigol DP832-class).

Ramps Vin with a soft start and captures the inrush current at 100 kS/s.
Swap for a pyvisa implementation; the phases stay unchanged.
"""

import numpy as np

SAMPLE_RATE_HZ = 100_000


class FixtureSupply:
    def __init__(self):
        self._volts = 0.0
        self._rng = np.random.default_rng(12)
        print("Fixture supply ready, output off")

    def ramp_to(self, volts, ramp_ms):
        """Soft-start ramp; returns (time_ms, vin_v, iin_ma) sampled at 100 kS/s over 200 ms."""
        self._volts = float(volts)
        n = int(0.2 * SAMPLE_RATE_HZ)
        t = np.arange(n) / SAMPLE_RATE_HZ * 1000.0
        vin = np.clip(volts * t / ramp_ms, 0.0, volts)
        # Bulk capacitor charge (C dV/dt) plus regulator start-up, then steady-state load.
        c_bulk_f = 470e-6
        dv_dt = np.gradient(vin, t / 1000.0)
        i_cap = c_bulk_f * dv_dt * 1000.0  # mA
        i_load = 90.0 * (1.0 - np.exp(-np.clip(t - 30.0, 0.0, None) / 12.0))
        iin = i_cap + i_load + self._rng.normal(0.0, 1.5, n)
        return t.tolist(), vin.tolist(), iin.tolist()

    def measure_current_ma(self):
        return 90.0 + self._rng.normal(0.0, 1.0)

    def measure_sleep_current_ua(self):
        """Low-range shunt engaged; DUT in stop mode."""
        return 7.8 + self._rng.normal(0.0, 0.3)

    def output_off(self):
        self._volts = 0.0

    def measure_voltage(self):
        return self._volts + self._rng.normal(0.0, 0.005)
