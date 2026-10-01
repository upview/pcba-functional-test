import numpy as np

from plugs.dut import ADC_BITS, ADC_FS_V
from utils.linearity import fit_linearity

STEPS_V = np.linspace(0.1, 3.2, 32)


def analog_linearity(measurements, dut, daq, ui, log):
    readings = []
    for i, v in enumerate(STEPS_V):
        daq.set_stimulus(float(v))
        code = dut.read_adc(float(v))
        readings.append(code / (2**ADC_BITS - 1) * ADC_FS_V)
        ui.sweep_progress = int((i + 1) / STEPS_V.size * 100)

    gain, offset_mv, r2 = fit_linearity(STEPS_V, readings)
    residual_mv = ((np.asarray(readings) - (gain * STEPS_V + offset_mv / 1000.0)) * 1000.0).tolist()
    log.info(f"ADC gain {gain:.4f}, offset {offset_mv:.1f} mV, R² {r2:.5f}")

    measurements.adc_sweep.x_axis = STEPS_V.tolist()
    measurements.adc_sweep.y_axis.reading = readings
    measurements.adc_sweep.y_axis.residual = residual_mv
    measurements.adc_sweep.y_axis.reading.aggregations.gain_error_pct = (gain - 1.0) * 100.0
    measurements.adc_sweep.y_axis.reading.aggregations.offset_mv = offset_mv
    measurements.adc_sweep.y_axis.reading.aggregations.r2 = r2
