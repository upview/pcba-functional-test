import numpy as np


def fit_linearity(stimulus_v, reading_v):
    """Least-squares fit reading = gain * stimulus + offset.

    Returns gain, offset in mV, R², and the residual of each point in mV.
    """
    x = np.asarray(stimulus_v, dtype=float)
    y = np.asarray(reading_v, dtype=float)
    gain, offset_v = np.polyfit(x, y, 1)
    residual_v = y - (gain * x + offset_v)
    r2 = 1.0 - np.sum(residual_v**2) / np.sum((y - y.mean()) ** 2)
    return float(gain), float(offset_v * 1000.0), float(r2), (residual_v * 1000.0).tolist()
