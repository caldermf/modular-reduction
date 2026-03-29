from __future__ import annotations

import pytest

from modular_reduction import KLSBasisSystem


pytestmark = pytest.mark.slow


def test_b3_table_matches_the_paper():
    system = KLSBasisSystem("B3")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0, 0),
        "s3": -character(0, 1, 24) + character(1, 0, 26),
        "s2": character(0, 26, 0) - character(0, 26, 2) + character(1, 27, 0),
        "s2*s3*s2": character(1, 26, 0) - character(0, 26, 2) + character(0, 28, 0),
        "s2*s3*s1*s2": -character(0, 26, 0) - character(1, 26, 0) + character(1, 27, 0) + character(0, 28, 0),
        "s2*s3*s1*s2*s3*s1*s2*s1": character(28, 27, 0) + character(28, 28, 0),
        "s3*s2*s3*s1*s2*s3*s2*s1": character(26, 0, 28) + character(27, 1, 26) + character(27, 0, 28) + character(28, 0, 28),
        "s3*s1*s2*s3*s2*s1": character(27, 0, 26) + character(28, 0, 26) + character(27, 1, 26) + character(29, 0, 26),
        "s3*s1*s2*s3*s1": -character(27, 0, 26) - character(26, 0, 28) + character(29, 0, 26) + character(28, 0, 28),
        "s1": character(25, 0, 0) - character(26, 0, 0),
        "s3*s1": character(27, 0, 26) - character(27, 1, 26) + character(28, 0, 28),
        "s1*s2*s3*s2*s1": -character(27, 0, 0) + character(28, 0, 0),
        "s1*s2*s1": -character(28, 27, 0) + character(28, 28, 0),
        "s1*s2*s3*s1*s2*s1": character(27, 28, 0) + character(29, 27, 0),
        "s3*s2*s3*s1*s2*s3*s1*s2": character(0, 28, 28),
        "s2*s3*s1*s2*s3*s1*s2": character(0, 26, 0) + character(0, 27, 0) + character(0, 26, 2) + character(0, 28, 0),
        "s3*s2*s3*s2": character(0, 27, 28),
        "s3*s2*s3*s1*s2*s3": character(0, 0, 24) + character(0, 0, 26) + character(0, 0, 28),
        "s3*s2*s3": -character(0, 0, 24) + character(0, 0, 28),
        "s3*s2*s3*s1*s2*s3*s1*s2*s1": character(28, 28, 28),
    }

    for word, value in expected.items():
        assert system.mw(system.context.element_from_word(word), 29) == value


def test_c3_table_matches_the_paper():
    system = KLSBasisSystem("C3")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0, 0),
        "s3": -character(0, 1, 26) + character(1, 0, 27),
        "s2": character(0, 25, 0) - character(1, 25, 1) + character(2, 26, 0),
        "s2*s3*s2": character(2, 25, 0) - character(1, 25, 1) + character(0, 28, 0),
        "s2*s3*s1*s2": -character(0, 25, 0) + character(0, 26, 0) - character(2, 25, 0) - character(0, 27, 0) + character(2, 26, 0) + character(0, 28, 0),
        "s2*s3*s1*s2*s3*s1*s2*s1": character(28, 26, 0) + character(28, 27, 0) + character(28, 28, 0),
        "s3*s2*s3*s1*s2*s3*s2*s1": character(26, 0, 28) + character(27, 1, 27) + character(28, 0, 28),
        "s3*s1*s2*s3*s2*s1": character(27, 0, 27) + character(27, 1, 27) + character(29, 0, 27),
        "s3*s1*s2*s3*s1": -character(27, 0, 27) - character(26, 0, 28) + character(29, 0, 27) + character(28, 0, 28),
        "s1": character(24, 0, 0) + character(26, 0, 0),
        "s3*s1": character(27, 0, 27) - character(27, 1, 27) + character(28, 0, 28),
        "s1*s2*s3*s2*s1": character(26, 0, 0) + character(28, 0, 0),
        "s1*s2*s1": -character(28, 26, 0) + character(28, 28, 0),
        "s1*s2*s3*s1*s2*s1": character(26, 28, 0) + character(28, 27, 0) + character(30, 26, 0),
        "s3*s2*s3*s1*s2*s3*s1*s2": character(0, 28, 28),
        "s2*s3*s1*s2*s3*s1*s2": character(0, 25, 0) + character(0, 26, 0) + character(1, 25, 1) + character(0, 27, 0) + character(0, 28, 0),
        "s3*s2*s3*s2": character(0, 27, 28),
        "s3*s2*s3*s1*s2*s3": character(0, 0, 26) + character(0, 0, 28),
        "s3*s2*s3": -character(0, 0, 26) + character(0, 0, 28),
        "s3*s2*s3*s1*s2*s3*s1*s2*s1": character(28, 28, 28),
    }

    for word, value in expected.items():
        assert system.mw(system.context.element_from_word(word), 29) == value


def test_d4_selected_rows_match_the_paper():
    system = KLSBasisSystem("D4")
    character = system.context.weyl_character

    expected = {
        "1": character(0, 0, 0, 0),
        "s4": -character(0, 0, 0, 24) + character(0, 0, 0, 28),
        "s1": -character(24, 0, 0, 0) + character(28, 0, 0, 0),
        "s2": character(0, 25, 0, 0) - character(0, 25, 2, 0) - character(0, 25, 0, 2) - character(2, 25, 0, 0) + 2 * character(1, 25, 1, 1) - character(0, 26, 2, 0) - character(0, 26, 0, 2) - character(2, 26, 0, 0) + character(0, 28, 0, 0),
        "s2*s3*s2": -character(0, 26, 28, 0) + character(0, 28, 26, 0),
        "s4*s1": -character(26, 0, 0, 26) + character(26, 1, 0, 26) - character(27, 0, 1, 27) + character(28, 0, 0, 28),
        "s4*s2*s3*s1*s2*s4*s1*s2*s3*s1*s2*s1": character(28, 28, 28, 28),
    }

    for word, value in expected.items():
        assert system.mw(system.context.element_from_word(word), 29) == value
