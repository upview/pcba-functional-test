def operator_checks(measurements, daq, log):
    """Photodiodes back the operator's checklist with numbers.

    The three switches in procedure.yaml write straight into their measurements
    through `bind:`, so this phase only reads the photodiodes.
    """
    measurements.status_led_mv = daq.photodiode_mv("status_green")
    measurements.fault_led_mv = daq.photodiode_mv("fault_red")
    log.info("LED photodiodes read")
