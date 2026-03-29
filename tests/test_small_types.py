from __future__ import annotations

from modular_reduction import KLSBasisSystem


def test_a1_mw_table_matches_the_paper():
    system = KLSBasisSystem("A1")
    character = system.context.weyl_character

    expected = {
        "1": character(0),
        "s1": character(10),
    }

    for word, character in expected.items():
        assert system.mw(system.context.element_from_word(word), 11) == character


def test_a2_mw_table_matches_the_paper():
    system = KLSBasisSystem("A2")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0),
        "s1": character(10, 0),
        "s2": character(0, 10),
        "s1*s2*s1": character(10, 10),
    }

    for word, character in expected.items():
        assert system.mw(system.context.element_from_word(word), 11) == character


def test_b2_mw_table_matches_the_paper():
    system = KLSBasisSystem("B2")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0),
        "s2*s1*s2": character(0, 28),
        "s2": character(0, 26),
        "s1": character(27, 0),
        "s2*s1*s2*s1": character(28, 28),
        "s1*s2*s1": character(28, 0),
    }

    for word, character in expected.items():
        assert system.mw(system.context.element_from_word(word), 29) == character


def test_g2_mw_table_matches_the_paper():
    system = KLSBasisSystem("G2")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0),
        "s1": character(25, 0),
        "s2": character(0, 27),
        "s1*s2*s1": character(25, 1),
        "s2*s1*s2": character(1, 27),
        "s1*s2*s1*s2*s1": character(28, 0),
        "s2*s1*s2*s1*s2": character(0, 28),
        "s2*s1*s2*s1*s2*s1": character(28, 28),
    }

    for word, character in expected.items():
        assert system.mw(system.context.element_from_word(word), 29) == character


def test_a3_mw_table_matches_the_paper():
    system = KLSBasisSystem("A3")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0, 0),
        "s1": character(28, 0, 0),
        "s3": character(0, 0, 28),
        "s2": character(0, 28, 0) - character(0, 26, 0),
        "s3*s1": character(28, 0, 28) - character(27, 0, 27),
        "s1*s2*s1": character(28, 28, 0),
        "s2*s3*s2": character(0, 28, 28),
        "s2*s3*s1*s2": character(0, 28, 0) + character(0, 26, 0),
        "s1*s2*s3*s2*s1": character(28, 0, 28) + character(27, 0, 27),
        "s1*s2*s3*s1*s2*s1": character(28, 28, 28),
    }

    for word, character in expected.items():
        assert system.mw(system.context.element_from_word(word), 29) == character


def test_b2_duflo_selection_is_computed_from_left_cells():
    system = KLSBasisSystem("B2")

    assert system.cells.duflo_involution(system.context.element_from_word("s1*s2*s1")) == system.context.element_from_word("s1")
    assert system.cells.duflo_involution(system.context.element_from_word("s2*s1*s2")) == system.context.element_from_word("s2")

def test_type_a_reduction_sums_the_correct_cell():
    system = KLSBasisSystem("A2")
    character = system.context.weyl_character

    assert system.reduction((3,), 11) == character(0, 0)
    assert system.reduction((2, 1), 11) == character(10, 0) + character(0, 10)
    assert system.reduction((1, 1, 1), 11) == character(10, 10)


def test_type_a_cell_involutions_are_partition_indexed():
    system = KLSBasisSystem("A2")

    assert {str(w) for w in system.type_a_cell_involutions((3,))} == {"1"}
    assert {str(w) for w in system.type_a_cell_involutions((2, 1))} == {"s1", "s2"}
    assert {str(w) for w in system.type_a_cell_involutions((1, 1, 1))} == {"s1*s2*s1"}


def test_export_layer_formats_rows_in_paper_style():
    system = KLSBasisSystem("A2")
    rows = system.mw_rows(11)

    assert rows[1].word == "s1"
    assert rows[1].character == "V_{10,0}"
    assert "Type $A_2$" in system.mw_latex_table(11)
    assert '"word": "s1"' in system.mw_json(11)
