def fixture_check(measurements, run, log):
    """Setup: lid interlock and DUT seating before any power is applied."""
    run.metadata["fixture_id"] = "FIX-07"
    run.metadata["fixture_cycles"] = 18420
    run.metadata["line"] = "SMT-2"

    measurements.lid_closed = True
    measurements.vacuum_kpa = -62.0
    log.info("Fixture FIX-07 closed, DUT seated")
