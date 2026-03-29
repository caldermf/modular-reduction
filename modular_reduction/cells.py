from __future__ import annotations

from functools import cached_property

from modular_reduction.catalog import (
    CURATED_LEFT_CELL_REPRESENTATIVE_MAPS,
    get_curated_representative_source,
)


class CellData:
    """Kazhdan-Lusztig cells and Duflo involutions computed through Sage."""

    def __init__(self, context):
        self.context = context

    @cached_property
    def left_cells(self):
        return tuple(
            frozenset(cell)
            for cell in self.context.weyl_group.kazhdan_lusztig_cells(side="left")
        )

    @cached_property
    def left_cell_of(self):
        mapping = {}
        for cell in self.left_cells:
            for element in cell:
                mapping[element] = cell
        return mapping

    @cached_property
    def duflo_by_left_cell(self):
        duflo = {}
        identity = self.context.identity
        kl = self.context.kl_polynomials

        for cell in self.left_cells:
            scores = {}
            for w in cell:
                scores[w] = w.length() - 2 * kl.P(identity, w).degree()

            minimum = min(scores.values())
            candidates = [w for w, value in scores.items() if value == minimum]
            if len(candidates) != 1:
                raise ValueError(
                    f"Expected a unique Duflo involution in left cell {cell}, found {candidates}."
                )
            duflo[cell] = candidates[0]

        return duflo

    def left_cell(self, w):
        return self.left_cell_of[w]

    def duflo_involution(self, w):
        return self.duflo_by_left_cell[self.left_cell(w)]

    @cached_property
    def curated_representative_source(self):
        return get_curated_representative_source(self.context.cartan_type)

    @cached_property
    def curated_representatives(self):
        source = self.curated_representative_source
        entries = {}
        if source is not None:
            entries = CURATED_LEFT_CELL_REPRESENTATIVE_MAPS.get(self.context.cartan_type, {})
        return {
            self.context.element_from_word(source): self.context.element_from_word(target)
            for source, target in entries.items()
        }

    def preferred_representative(self, w):
        if self.context.cartan_type[0] == "A":
            return w
        if w in self.curated_representatives:
            return self.curated_representatives[w]
        if w * w == self.context.identity:
            return w
        return self.duflo_involution(w)

    def is_near_involution(self, w) -> bool:
        return self.left_cell(w.inverse()) == self.left_cell(w)

    @cached_property
    def near_involutions(self):
        return tuple(w for w in self.context.elements if self.is_near_involution(w))
