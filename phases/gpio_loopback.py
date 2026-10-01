from plugs.daq import GPIO_CHANNELS


def gpio_loopback(measurements, dut, daq, ui, log):
    failed = []
    for ch in range(GPIO_CHANNELS):
        for level in (1, 0):
            dut.set_gpio(ch, level)
            daq.drive_gpio_from_dut(ch, level)  # mock: the loopback jumper
            if daq.read_gpio(ch) != level:
                failed.append(ch)
                break
        ui.loopback_progress = int((ch + 1) / GPIO_CHANNELS * 100)

    measurements.gpio_pass_count = GPIO_CHANNELS - len(failed)
    measurements.gpio_failed_channels = failed
    log.info(f"GPIO loopback: {GPIO_CHANNELS - len(failed)}/{GPIO_CHANNELS} channels")
