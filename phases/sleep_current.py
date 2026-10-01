def sleep_current(measurements, dut, psu, log):
    measurements.stop_mode_entered = dut.enter_stop_mode()
    ua = psu.measure_sleep_current_ua()
    log.info(f"Stop-mode current {ua:.1f} uA")
    measurements.sleep_current = ua
