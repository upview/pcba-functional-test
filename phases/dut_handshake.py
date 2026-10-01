def dut_handshake(measurements, dut, unit, log):
    """Put the firmware in test mode and record what is on the board."""
    measurements.test_mode = dut.enter_test_mode()
    firmware = dut.firmware_version()
    hardware = dut.hardware_revision()

    measurements.firmware_version = firmware
    measurements.hardware_revision = hardware
    unit.metadata["firmware_version"] = firmware
    log.info(f"DUT in test mode, firmware {firmware}, hardware rev {hardware}")
