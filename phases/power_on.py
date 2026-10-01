import numpy as np

RAMP_MS = 50.0


def power_on(measurements, psu, daq, log):
    t_ms, vin, iin = psu.ramp_to(12.0, RAMP_MS)
    iin = np.asarray(iin)
    settled = np.asarray(t_ms) > 150.0

    measurements.inrush.x_axis = t_ms
    measurements.inrush.y_axis.vin = vin
    measurements.inrush.y_axis.iin = iin.tolist()
    measurements.inrush.y_axis.iin.aggregations.peak_ma = float(iin.max())
    measurements.inrush.y_axis.iin.aggregations.steady_ma = float(iin[settled].mean())
    log.info(f"Inrush peak {iin.max():.0f} mA, steady {iin[settled].mean():.0f} mA")

    measurements.rail_3v3 = daq.measure_rail("3v3")
    measurements.rail_5v = daq.measure_rail("5v")
    measurements.rail_1v8 = daq.measure_rail("1v8")
    measurements.ripple_3v3 = daq.measure_ripple_mv("3v3")
