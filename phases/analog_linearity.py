import numpy as np

from utils.linearity import fit_linearity

STEPS_V = np.linspace(0.1, 3.2, 32)


def analog_linearity(measurements, dut, daq, ui, log):
    """Sweep the fixture stimulus across the ADC range and fit gain, offset and R²."""
    readings_v = []
    for i, volts in enumerate(STEPS_V):
        daq.set_stimulus(volts)
        readings_v.append(dut.read_adc_volts())
        ui.sweep_progress = int((i + 1) / STEPS_V.size * 100)

    gain, offset_mv, r2, residual_mv = fit_linearity(STEPS_V, readings_v)
    log.info(f"ADC gain {gain:.4f}, offset {offset_mv:.1f} mV, R² {r2:.5f}")

    measurements.adc_sweep.x_axis = STEPS_V.tolist()
    measurements.adc_sweep.y_axis.reading = readings_v
    measurements.adc_sweep.y_axis.residual = residual_mv
    measurements.adc_sweep.y_axis.reading.aggregations.gain_error_pct = (gain - 1.0) * 100.0
    measurements.adc_sweep.y_axis.reading.aggregations.offset_mv = offset_mv
    measurements.adc_sweep.y_axis.reading.aggregations.r2 = r2
