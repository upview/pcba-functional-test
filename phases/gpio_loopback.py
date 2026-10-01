from plugs.daq import GPIO_CHANNELS


def gpio_loopback(measurements, dut, daq, ui, log):
    """DUT drives each GPIO high then low; the fixture reads it back through the loopback."""
    failed = []
    for channel in range(GPIO_CHANNELS):
        for level in (1, 0):
            dut.set_gpio(channel, level)
            if daq.read_gpio(channel) != level:
                failed.append(channel)
                break
        ui.loopback_progress = int((channel + 1) / GPIO_CHANNELS * 100)

    measurements.gpio_pass_count = GPIO_CHANNELS - len(failed)
    measurements.gpio_failed_channels = failed
    log.info(f"GPIO loopback: {GPIO_CHANNELS - len(failed)}/{GPIO_CHANNELS} channels")
