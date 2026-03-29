from __future__ import annotations

from functools import cached_property, lru_cache

from modular_reduction.api import BasisDatum, BasisDataset, PublishedMWTable, TypeAReductionResult
from modular_reduction.catalog import get_published_table_source, get_type_a_reduction_source
from modular_reduction.cells import CellData
from modular_reduction.context import SageContext
from modular_reduction.export import mw_json, mw_latex_table, mw_rows
from modular_reduction.type_a import cell_involutions as type_a_cell_involutions
from modular_reduction.type_a import element_shape as type_a_element_shape
from modular_reduction.type_a import normalize_partition
from modular_reduction.type_a import reduction as type_a_reduction


class KLSBasisSystem:
    """Sage-native computations for the Kazhdan-Lusztig-Steinberg setup."""

    def __init__(self, cartan_type, prefix: str = "s"):
        if isinstance(cartan_type, SageContext):
            self.context = cartan_type
        else:
            self.context = SageContext(cartan_type, prefix=prefix)
        self.cells = CellData(self.context)

    def right_descent_indices(self, w) -> tuple[int, ...]:
        return tuple(i for i in range(1, self.context.rank + 1) if w.has_right_descent(i))

    def complementary_right_descent_indices(self, w) -> tuple[int, ...]:
        return tuple(i for i in range(1, self.context.rank + 1) if not w.has_right_descent(i))

    def weight_monomial(self, indices: tuple[int, ...]):
        out = self.context.weight_ring.one()
        for index in indices:
            out *= self.context.weight_ring(self.context.fundamental_weight(index))
        return out

    @lru_cache(maxsize=None)
    def parabolic_order(self, indices: tuple[int, ...]) -> int:
        if not indices:
            return 1
        generators = [self.context.simple_reflections[index] for index in indices]
        return self.context.weyl_group.subgroup(generators).cardinality()

    @lru_cache(maxsize=None)
    def kl_value_at_one(self, x, y) -> int:
        return int(self.context.kl_polynomials.P(x, y)(1))

    def _c_prime_apply(self, w, monomial):
        total = 0
        for y in self.context.weyl_group.bruhat_interval(self.context.identity, w):
            total += self.kl_value_at_one(y, w) * monomial.weyl_group_action(y)
        return total

    def _c_dual_apply(self, w, monomial):
        total = 0
        target = self.context.long_element * w
        for y in self.context.weyl_group.bruhat_interval(self.context.identity, target):
            total += self.kl_value_at_one(y, target) * monomial.weyl_group_action(
                self.context.long_element * y
            )
        return total

    @lru_cache(maxsize=None)
    def basis_element(self, w):
        descents = self.right_descent_indices(w)
        complement = self.complementary_right_descent_indices(w)
        return self._c_prime_apply(w, self.weight_monomial(complement)) / self.parabolic_order(descents)

    @lru_cache(maxsize=None)
    def frobenius_basis_element(self, w, q_value: int):
        descents = self.right_descent_indices(w)
        complement = self.complementary_right_descent_indices(w)
        return self._c_prime_apply(
            w, self.weight_monomial(complement).scale(q_value)
        ) / self.parabolic_order(descents)

    @lru_cache(maxsize=None)
    def pseudo_dual_element(self, w):
        descents = self.right_descent_indices(w)
        complement = self.complementary_right_descent_indices(w)
        return self._c_dual_apply(w, self.weight_monomial(descents)) / self.parabolic_order(
            complement
        )

    @lru_cache(maxsize=None)
    def _weight_pairing(self, weight):
        reduced = self.context.weyl_character_ring.dot_reduce(weight - self.context.rho)
        if reduced[0] == 0:
            return 0
        return reduced[0] * self.context.weyl_character_ring(reduced[1])

    def pairing(self, left, right):
        total = 0
        coefficients = dict(self.context.weight_ring(left * right))
        for weight, coefficient in coefficients.items():
            total += coefficient * self._weight_pairing(weight)
        return total

    @cached_property
    def gram_matrix(self):
        return tuple(
            tuple(
                self.pairing(self.basis_element(left), self.pseudo_dual_element(right))
                for right in self.context.elements
            )
            for left in self.context.elements
        )

    @cached_property
    def upper_triangular_order(self):
        remaining = list(range(len(self.context.elements)))
        order = []
        while remaining:
            for candidate in list(remaining):
                if all(
                    other == candidate or self.gram_matrix[other][candidate] == 0
                    for other in remaining
                ):
                    order.append(candidate)
                    remaining.remove(candidate)
        order.reverse()
        return tuple(order)

    def _diagonal_scalar(self, index: int):
        diagonal = self.gram_matrix[index][index]
        coefficients = dict(self.context.weyl_character_ring(diagonal))
        if len(coefficients) != 1:
            raise ValueError(
                f"Expected a single-term diagonal pairing for index {index}, found {diagonal}."
            )
        return next(iter(coefficients.values()))

    @cached_property
    def dual_basis(self):
        dual = {}
        elements = self.context.elements
        for target_index in self.upper_triangular_order:
            target = elements[target_index]
            candidate = self.pseudo_dual_element(target) / self._diagonal_scalar(target_index)
            for source_index in self.upper_triangular_order:
                source = elements[source_index]
                coefficient = self.pairing(self.basis_element(source), candidate)
                if source_index != target_index and coefficient != 0:
                    candidate -= (
                        coefficient
                        * self.pseudo_dual_element(source)
                        / self._diagonal_scalar(source_index)
                    )
            dual[target] = candidate
        return dual

    def dual_basis_element(self, w):
        return self.dual_basis[w]

    def is_near_involution(self, w) -> bool:
        return self.cells.is_near_involution(w)

    def near_involutions(self):
        return self.cells.near_involutions

    def _type_a_mw(self, w, q_value: int):
        if not self.is_near_involution(w):
            raise ValueError(f"{w} is not a near involution.")
        duflo = self.cells.duflo_involution(w)
        return self.pairing(
            self.frobenius_basis_element(self.context.long_element * duflo, q_value),
            self.dual_basis_element(self.context.long_element * w),
        )

    def _type_a_pseudo_mw(self, w, q_value: int):
        if not self.is_near_involution(w):
            raise ValueError(f"{w} is not a near involution.")
        duflo = self.cells.duflo_involution(w)
        return self.pairing(
            self.frobenius_basis_element(self.context.long_element * duflo, q_value),
            self.pseudo_dual_element(self.context.long_element * w),
        )

    def mw(self, w, q_value: int):
        """Compute the published M_w values."""
        if not self.is_near_involution(w):
            raise ValueError(f"{w} is not a near involution.")
        if self.context.cartan_type[0] == "A":
            return self._type_a_mw(w, q_value)
        shifted = self.context.long_element * w
        representative = self.cells.preferred_representative(shifted)
        return self.pairing(
            self.frobenius_basis_element(shifted, q_value),
            self.dual_basis_element(representative),
        )

    def pseudo_mw(self, w, q_value: int):
        if not self.is_near_involution(w):
            raise ValueError(f"{w} is not a near involution.")
        if self.context.cartan_type[0] == "A":
            return self._type_a_pseudo_mw(w, q_value)
        shifted = self.context.long_element * w
        representative = self.cells.preferred_representative(shifted)
        return self.pairing(
            self.frobenius_basis_element(shifted, q_value),
            self.pseudo_dual_element(representative),
        )

    def published_table_source(self):
        return get_published_table_source(self.context.cartan_type)

    def type_a_reduction_source(self):
        if self.context.cartan_type[0] != "A":
            return None
        return get_type_a_reduction_source()

    def mw_table(self, q_value: int):
        return {w: self.mw(w, q_value) for w in self.cells.near_involutions}

    def mw_rows(self, q_value: int):
        return mw_rows(self.mw_table(q_value))

    def mw_json(self, q_value: int) -> str:
        return mw_json(self.mw_table(q_value))

    def mw_latex_table(self, q_value: int) -> str:
        return mw_latex_table(self.context.cartan_type, self.mw_table(q_value))

    def published_table(self, q_value: int) -> PublishedMWTable:
        table = self.mw_table(q_value)
        entries = tuple((str(element), value) for element, value in table.items())
        return PublishedMWTable(
            cartan_type=self.context.cartan_type,
            q_value=q_value,
            entries=entries,
            rows=mw_rows(table),
            source=self.published_table_source(),
        )

    def basis_data(
        self,
        *,
        only_near_involutions: bool = False,
        q_value: int | None = None,
    ) -> BasisDataset:
        elements = self.cells.near_involutions if only_near_involutions else self.context.elements
        data = []
        for w in elements:
            is_near = self.is_near_involution(w)
            datum = BasisDatum(
                word=str(w),
                right_descents=self.right_descent_indices(w),
                is_near_involution=is_near,
                duflo_involution=str(self.cells.duflo_involution(w)),
                preferred_representative=str(self.cells.preferred_representative(w)),
                basis=self.basis_element(w),
                pseudo_dual=self.pseudo_dual_element(w),
                dual=self.dual_basis_element(w),
                type_a_shape=(
                    self.type_a_shape(w) if self.context.cartan_type[0] == "A" else None
                ),
                mw_value=self.mw(w, q_value) if is_near and q_value is not None else None,
            )
            data.append(datum)
        return BasisDataset(
            cartan_type=self.context.cartan_type,
            only_near_involutions=only_near_involutions,
            q_value=q_value,
            data=tuple(data),
            representative_source=self.cells.curated_representative_source,
        )

    def type_a_shape(self, w) -> tuple[int, ...]:
        if self.context.cartan_type[0] != "A":
            raise ValueError("Robinson-Schensted cell shapes are only defined here for Type A.")
        return type_a_element_shape(w)

    def type_a_cell_involutions(self, partition) -> tuple:
        return type_a_cell_involutions(self, partition)

    def reduction(self, partition, q_value: int):
        """Brauer reduction in Type A for the partition-indexed unipotent representation."""
        return type_a_reduction(self, partition, q_value)

    def reduction_data(self, partition, q_value: int) -> TypeAReductionResult:
        normalized = self.normalize_partition(partition)
        terms = []
        for w in self.type_a_cell_involutions(normalized):
            terms.append(
                (
                    w,
                    self.mw(w, q_value),
                )
            )
        return TypeAReductionResult(
            cartan_type=self.context.cartan_type,
            partition=normalized,
            q_value=q_value,
            value=type_a_reduction(self, normalized, q_value),
            terms=mw_rows(dict(terms)),
            source=self.type_a_reduction_source(),
        )

    def normalize_partition(self, partition) -> tuple[int, ...]:
        if self.context.cartan_type[0] != "A":
            raise ValueError("Partition normalization is only defined here for Type A.")
        return normalize_partition(partition, self.context.rank + 1)
