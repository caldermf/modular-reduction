from __future__ import annotations

from modular_reduction.__main__ import main


def test_supported_command_lists_verified_types(capsys):
    assert main(["supported"]) == 0
    output = capsys.readouterr().out

    assert "Published paper tables:" in output
    assert "A3" in output
    assert "G2" in output
    assert "Curated left-cell representatives:" in output


def test_provenance_command_reports_paper_metadata(capsys):
    assert main(["provenance", "A2"]) == 0
    output = capsys.readouterr().out

    assert "Cartan type: A2" in output
    assert "Published table:" in output
    assert "minimal_master_A2.ipynb" in output


def test_reduction_command_supports_json_output(capsys):
    assert main(["reduction", "A2", "11", "2,1", "--format", "json"]) == 0
    output = capsys.readouterr().out

    assert '"partition": [' in output
    assert '"character":' in output
    assert 'V_{10,0}' in output
    assert 'V_{0,10}' in output
