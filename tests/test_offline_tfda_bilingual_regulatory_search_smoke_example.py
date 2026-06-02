from __future__ import annotations

import subprocess
import sys


def test_offline_tfda_bilingual_regulatory_search_smoke_example_runs():
    completed = subprocess.run(
        [sys.executable, "examples/offline_tfda_bilingual_regulatory_search_smoke.py"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert "offline TFDA bilingual regulatory search smoke passed" in completed.stdout
    assert "TFDA bilingual query retrieval for mRNA疫苗" in completed.stdout
    assert "TFDA bilingual query retrieval for 抗體藥物複合體 ADC" in completed.stdout
    assert "TFDA bilingual query retrieval for 生物相似性藥品" in completed.stdout
    assert "TFDA bilingual no-result behavior after modality filtering" in completed.stdout
