def fixture_check(measurements, daq, run, log):
    """Setup: lid interlock and DUT seating, checked before any power is applied."""
    run.metadata["fixture_id"] = "FIX-07"
    run.metadata["line"] = "SMT-2"

    measurements.lid_closed = daq.lid_closed()
    measurements.vacuum_kpa = daq.vacuum_kpa()
    log.info("Fixture FIX-07 closed, DUT seated")
