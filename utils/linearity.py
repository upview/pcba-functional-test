import numpy as np


def fit_linearity(stimulus_v, reading_v):
    """Least-squares fit reading = gain * stimulus + offset; returns gain, offset_mv, r2."""
    x = np.asarray(stimulus_v, dtype=float)
    y = np.asarray(reading_v, dtype=float)
    gain, offset = np.polyfit(x, y, 1)
    pred = gain * x + offset
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return float(gain), float(offset * 1000.0), 1.0 - ss_res / ss_tot
