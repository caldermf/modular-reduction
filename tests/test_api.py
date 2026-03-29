from __future__ import annotations

from modular_reduction import (
    KLSBasisSystem,
    basis_data,
    provenance,
    published_cartan_types,
    published_table,
    type_a_reduction,
)


def test_published_table_api_carries_provenance():
    table = published_table("A2", 11)

    assert table.source is not None
    assert table.source.provenance.kind == "published_mw_table"
    assert table.characters_by_word()["s1"] == "V_{10,0}"
    assert "Type $A_2$" in table.latex()


def test_basis_data_api_exposes_curated_representatives_and_mw_values():
    dataset = basis_data("B2", only_near_involutions=True, q_value=29)

    assert dataset.representative_source is not None
    assert dataset.representative_source.provenance.kind == "curated_left_cell_representatives"

    singular = next(datum for datum in dataset.data if datum.word == "s1*s2*s1")
    assert singular.preferred_representative == "s1"
    assert singular.duflo_involution == "s1"
    assert singular.as_dict()["mw"] == "V_{28,0}"


def test_type_a_reduction_result_lists_partition_summands():
    result = type_a_reduction("A2", (2, 1), 11)

    assert result.partition == (2, 1)
    assert result.source.kind == "type_a_reduction"
    assert {term.word for term in result.terms} == {"s1", "s2"}
    assert {term.character for term in result.terms} == {"V_{10,0}", "V_{0,10}"}


def test_basis_data_records_type_a_shapes():
    dataset = KLSBasisSystem("A2").basis_data(only_near_involutions=True, q_value=11)

    s1 = next(datum for datum in dataset.data if datum.word == "s1")
    assert s1.type_a_shape == (2, 1)
    assert s1.as_dict()["mw"] == "V_{10,0}"


def test_supported_types_and_provenance_are_public():
    assert ("A", 3) in published_cartan_types()

    report = provenance("A3")
    assert report.published_table is not None
    assert report.published_table.provenance.notebook_path == "minimal_master_A3.ipynb"
