from __future__ import annotations

import subprocess
import sys


def test_offline_product_modality_regulatory_search_smoke_example_runs():
    completed = subprocess.run(
        [sys.executable, "examples/offline_product_modality_regulatory_search_smoke.py"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert "offline product modality regulatory search smoke passed" in completed.stdout
    assert "FDA product_modality string filter" in completed.stdout
    assert "TFDA product_modality filter" in completed.stdout
