"""Simulated wiring between the mock plugs.

On a real fixture the DUT and the DAQ are wired together: a GPIO the DUT
drives shows up on a DAQ input, a voltage the DAQ outputs reaches a DUT ADC
pin. Each plug runs in its own process, so the two mocks share a small state
directory to simulate those wires. The phases read exactly like they would
against real hardware. Delete this file when the real plugs land.
"""

import json
import os
import tempfile
from pathlib import Path

_DIR = Path(tempfile.gettempdir()) / "pcba-fct-mock-wiring"
_DIR.mkdir(exist_ok=True)


def write(wire, value):
    # One file per wire, replaced atomically: phases run in parallel.
    tmp = _DIR / f"{wire}.{os.getpid()}.tmp"
    tmp.write_text(json.dumps(value))
    os.replace(tmp, _DIR / f"{wire}.json")


def read(wire, default):
    path = _DIR / f"{wire}.json"
    return json.loads(path.read_text()) if path.exists() else default
