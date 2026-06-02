from __future__ import annotations

import subprocess
import sys


def test_offline_query_metadata_consistency_smoke_example_runs():
    completed = subprocess.run(
        [sys.executable, "examples/offline_query_metadata_consistency_smoke.py"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert "offline query metadata consistency smoke passed" in completed.stdout
    assert "FDA regulatory record metadata contract" in completed.stdout
    assert "TFDA regulatory record metadata contract" in completed.stdout
    assert "query_metadata filters_applied date_range contract" in completed.stdout
    assert "FDA/TFDA normalized record key consistency" in completed.stdout
