# PCBA Functional Test

A TofuPilot Framework procedure for a pogo-pin PCBA functional test: fixture check, soft-start power-on with inrush capture, rail and ripple checks, firmware handshake over UART, GPIO loopback, ADC linearity sweep, operator visual checks, sleep current, and power-down.

The instruments are mocked, so it runs on any machine.

## Run It

```bash
uv sync                                       # create the venv
tofupilot run . --kiosk                       # with the operator UI
tofupilot run . --json --ui-values ui.json    # unattended
```

## Structure

| Path | What it holds |
|------|---------------|
| `procedure.yaml` | The sequence: phases, measurements, limits, operator UI |
| `phases/` | One Python file per phase: the test logic |
| `plugs/` | Instrument drivers: supply, DAQ, DUT serial (mocked) |
| `utils/linearity.py` | Least-squares fit for the ADC sweep |
| `ui.json` | Operator answers for unattended runs |

## Use Real Hardware

Replace the mocks in `plugs/`: `psu.py` with pyvisa, `daq.py` with nidaqmx, `dut.py` with pyserial. Delete `plugs/mock_wiring.py`, which only simulates the wiring between the mocks. The phases, measurements and limits stay the same.
