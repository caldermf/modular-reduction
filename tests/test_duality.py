from __future__ import annotations

import pytest

from modular_reduction import KLSBasisSystem


@pytest.mark.slow
def test_a4_true_dual_differs_from_pseudo_dual_for_s232():
    system = KLSBasisSystem("A4")
    wcr = system.context.weyl_character_ring
    target = system.context.element_from_word("s2*s3*s2")

    assert system.dual_basis_element(target) != system.pseudo_dual_element(target)
    assert system.mw(target, 29) == wcr(0, 28, 28, 0) - wcr(0, 27, 27, 0)
    assert system.pseudo_mw(target, 29) != system.mw(target, 29)
