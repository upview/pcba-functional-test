def sleep_current(measurements, dut, psu, log):
    """Put the DUT in stop mode and measure its current on the low-range shunt."""
    measurements.stop_mode_entered = dut.enter_stop_mode()
    sleep_ua = psu.measure_sleep_current_ua()
    measurements.sleep_current = sleep_ua
    log.info(f"Stop-mode current {sleep_ua:.1f} µA")
