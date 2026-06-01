from __future__ import annotations

import subprocess
import sys


def test_offline_regulatory_date_range_smoke_example_runs():
    completed = subprocess.run(
        [sys.executable, "examples/offline_regulatory_date_range_smoke.py"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert "offline regulatory date range smoke passed" in completed.stdout
    assert "date_range='1m'" in completed.stdout
    assert "date_range='custom'" in completed.stdout
    assert "date_from / date_to backward compatibility" in completed.stdout
    assert "ambiguous date input rejection" in completed.stdout
