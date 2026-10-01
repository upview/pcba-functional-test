"""Programmable DC supply on the fixture Vin rail (mock Rigol DP832-class).

Ramps Vin with a soft start and captures the inrush current at 100 kS/s.
Swap for a pyvisa implementation; the phases stay unchanged.
"""

import numpy as np

SAMPLE_RATE_HZ = 100_000
CAPTURE_MS = 200.0
BULK_CAPACITANCE_F = 470e-6


class FixtureSupply:
    def __init__(self):
        self._volts = 0.0
        self._rng = np.random.default_rng()
        self._load_ma = 90.0 + self._rng.normal(0.0, 3.0)
        print("Fixture supply ready, output off")

    def ramp_to(self, volts, ramp_ms):
        """Soft-start ramp; returns (time_ms, vin_v, iin_ma) over the capture window."""
        self._volts = float(volts)
        n = int(CAPTURE_MS / 1000.0 * SAMPLE_RATE_HZ)
        t_ms = np.arange(n) / SAMPLE_RATE_HZ * 1000.0
        vin = np.clip(volts * t_ms / ramp_ms, 0.0, volts)
        # Bulk capacitor charge (C dV/dt) plus regulator start-up, then steady-state load.
        i_cap = BULK_CAPACITANCE_F * np.gradient(vin, t_ms / 1000.0) * 1000.0
        i_load = self._load_ma * (1.0 - np.exp(-np.clip(t_ms - 30.0, 0.0, None) / 12.0))
        iin = i_cap + i_load + self._rng.normal(0.0, 1.5, n)
        return t_ms.tolist(), vin.tolist(), iin.tolist()

    def measure_sleep_current_ua(self):
        """Low-range shunt engaged; DUT in stop mode."""
        return 7.8 + self._rng.normal(0.0, 0.6)

    def output_off(self):
        self._volts = 0.0

    def measure_voltage(self):
        return self._volts + self._rng.normal(0.0, 0.005)
