from __future__ import annotations

import subprocess
import sys


def test_offline_clinical_trial_query_metadata_consistency_smoke_example_runs():
    completed = subprocess.run(
        [sys.executable, "examples/offline_clinical_trial_query_metadata_consistency_smoke.py"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert "offline clinical trial query metadata consistency smoke passed" in completed.stdout
    assert "ClinicalTrials.gov normalized trial metadata contract" in completed.stdout
    assert "clinical trial indication query metadata contract" in completed.stdout
    assert "clinical trial sponsor/company query metadata contract" in completed.stdout
    assert "clinical trial official_url and results_available fields" in completed.stdout
