from __future__ import annotations

import re
from functools import cached_property

from sage.all import CartanType, LaurentPolynomialRing, QQ, WeightRing, WeylCharacterRing, WeylGroup
from sage.combinat.kazhdan_lusztig import KazhdanLusztigPolynomial


def _normalize_cartan_type(cartan_type):
    if isinstance(cartan_type, str):
        match = re.fullmatch(r"\s*([A-Za-z]+)\s*([0-9]+)\s*", cartan_type)
        if match is None:
            raise ValueError(
                f"Could not parse Cartan type {cartan_type!r}. Expected forms like 'A4' or ('A', 4)."
            )
        return (match.group(1).upper(), int(match.group(2)))

    if isinstance(cartan_type, (tuple, list)) and len(cartan_type) == 2:
        return (str(cartan_type[0]).upper(), int(cartan_type[1]))

    raise TypeError(
        f"Unsupported Cartan type specification {cartan_type!r}. Expected a string like 'A4' or a pair."
    )


class SageContext:
    """Shared Sage objects for a fixed Cartan type."""

    def __init__(self, cartan_type, prefix: str = "s"):
        self._cartan_type = _normalize_cartan_type(cartan_type)
        self.prefix = prefix

    @property
    def cartan_type(self) -> tuple[str, int]:
        return self._cartan_type

    @cached_property
    def cartan(self):
        return CartanType(list(self._cartan_type))

    @cached_property
    def weyl_group(self):
        return WeylGroup(self.cartan, prefix=self.prefix)

    @cached_property
    def simple_reflections(self):
        return self.weyl_group.simple_reflections()

    @cached_property
    def identity(self):
        return self.simple_reflections[1] ** 2

    @cached_property
    def long_element(self):
        return self.weyl_group.long_element()

    @cached_property
    def rank(self) -> int:
        return len(self.simple_reflections)

    @cached_property
    def elements(self):
        return tuple(self.weyl_group)

    @cached_property
    def q_ring(self):
        return LaurentPolynomialRing(QQ, "q")

    @cached_property
    def q_symbol(self):
        return self.q_ring.gen()

    @cached_property
    def kl_polynomials(self):
        return KazhdanLusztigPolynomial(self.weyl_group, self.q_symbol)

    @cached_property
    def weyl_character_ring(self):
        return WeylCharacterRing(self.cartan, style="coroots", base_ring=QQ)

    @cached_property
    def weight_ring(self):
        return WeightRing(self.weyl_character_ring)

    @cached_property
    def fundamental_weights(self):
        return tuple(weight.coerce_to_sl() for weight in self.weyl_character_ring.fundamental_weights())

    @cached_property
    def rho(self):
        total = 0
        for weight in self.fundamental_weights:
            total += weight
        return total

    def fundamental_weight(self, index: int):
        return self.fundamental_weights[index - 1]

    def element_from_word(self, word: str):
        word = word.strip()
        if word in {"", "1"}:
            return self.identity

        element = self.identity
        for token in word.split("*"):
            token = token.strip()
            if not token or token == "1":
                continue
            if not token.startswith(self.prefix):
                raise ValueError(f"Unrecognized token {token!r} in word {word!r}.")
            index = int(token[len(self.prefix) :])
            element *= self.simple_reflections[index]
        return element

    def weyl_character(self, *coords):
        return self.weyl_character_ring(tuple(coords))
