def power_down(measurements, psu, log):
    """Teardown: Vin off before the lid opens, whatever happened before."""
    psu.output_off()
    measurements.vin_off = abs(psu.measure_voltage())
    log.info("Vin off")
