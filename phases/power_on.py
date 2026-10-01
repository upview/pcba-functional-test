import numpy as np

VIN_V = 12.0
RAMP_MS = 50.0
SETTLED_AFTER_MS = 150.0


def power_on(measurements, psu, daq, log):
    """Soft-start Vin, capture the inrush current, then check every rail."""
    t_ms, vin, iin = psu.ramp_to(VIN_V, RAMP_MS)
    iin = np.asarray(iin)
    settled = np.asarray(t_ms) > SETTLED_AFTER_MS
    peak_ma = float(iin.max())
    steady_ma = float(iin[settled].mean())

    measurements.inrush.x_axis = t_ms
    measurements.inrush.y_axis.vin = vin
    measurements.inrush.y_axis.iin = iin.tolist()
    measurements.inrush.y_axis.iin.aggregations.peak_ma = peak_ma
    measurements.inrush.y_axis.iin.aggregations.steady_ma = steady_ma
    log.info(f"Inrush peak {peak_ma:.0f} mA, steady {steady_ma:.0f} mA")

    measurements.rail_3v3 = daq.measure_rail("3v3")
    measurements.rail_5v = daq.measure_rail("5v")
    measurements.rail_1v8 = daq.measure_rail("1v8")
    measurements.ripple_3v3 = daq.measure_ripple_mvpp("3v3")
