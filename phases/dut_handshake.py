def dut_handshake(measurements, dut, unit, log):
    measurements.test_mode = dut.enter_test_mode()
    version = dut.firmware_version()
    measurements.firmware_version = version
    measurements.hardware_revision = dut.hardware_revision()
    unit.metadata["firmware_version"] = version
    log.info(f"DUT in test mode, firmware {version}, hardware rev {dut.hardware_revision()}")
