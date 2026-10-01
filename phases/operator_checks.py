def operator_checks(measurements, daq, log):
    """Photodiode readings back the operator's checklist with numbers."""
    measurements.status_led_mv = daq.photodiode_mv("status_green")
    measurements.fault_led_mv = daq.photodiode_mv("fault_red")
    log.info("LED photodiodes read; operator switches recorded through their bindings")
