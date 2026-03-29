from __future__ import annotations

import json
from dataclasses import dataclass

from modular_reduction.catalog import (
    CuratedRepresentativeSource,
    PublishedTableSource,
    ProvenanceRecord,
)
from modular_reduction.export import MWTableRow, character_to_paper_string, mw_latex_table


@dataclass(frozen=True)
class BasisDatum:
    word: str
    right_descents: tuple[int, ...]
    is_near_involution: bool
    duflo_involution: str
    preferred_representative: str
    basis: object
    pseudo_dual: object
    dual: object
    type_a_shape: tuple[int, ...] | None = None
    mw_value: object | None = None

    def as_dict(self) -> dict[str, object]:
        data = {
            "word": self.word,
            "right_descents": self.right_descents,
            "is_near_involution": self.is_near_involution,
            "duflo_involution": self.duflo_involution,
            "preferred_representative": self.preferred_representative,
            "basis": str(self.basis),
            "pseudo_dual": str(self.pseudo_dual),
            "dual": str(self.dual),
            "type_a_shape": self.type_a_shape,
        }
        if self.mw_value is not None:
            data["mw"] = character_to_paper_string(self.mw_value)
        return data


@dataclass(frozen=True)
class BasisDataset:
    cartan_type: tuple[str, int]
    only_near_involutions: bool
    q_value: int | None
    data: tuple[BasisDatum, ...]
    representative_source: CuratedRepresentativeSource | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "cartan_type": self.cartan_type,
            "only_near_involutions": self.only_near_involutions,
            "q_value": self.q_value,
            "representative_source": None
            if self.representative_source is None
            else self.representative_source.as_dict(),
            "data": [datum.as_dict() for datum in self.data],
        }

    def json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)


@dataclass(frozen=True)
class PublishedMWTable:
    cartan_type: tuple[str, int]
    q_value: int
    entries: tuple[tuple[str, object], ...]
    rows: tuple[MWTableRow, ...]
    source: PublishedTableSource | None = None

    def by_word(self) -> dict[str, object]:
        return dict(self.entries)

    def characters_by_word(self) -> dict[str, str]:
        return {word: character_to_paper_string(value) for word, value in self.entries}

    def latex(self) -> str:
        return mw_latex_table(self.cartan_type, self.by_word())

    def json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)

    def as_dict(self) -> dict[str, object]:
        return {
            "cartan_type": self.cartan_type,
            "q_value": self.q_value,
            "source": None if self.source is None else self.source.as_dict(),
            "rows": [row.as_dict() for row in self.rows],
        }


@dataclass(frozen=True)
class TypeAReductionResult:
    cartan_type: tuple[str, int]
    partition: tuple[int, ...]
    q_value: int
    value: object
    terms: tuple[MWTableRow, ...]
    source: ProvenanceRecord

    @property
    def character(self) -> str:
        return character_to_paper_string(self.value)

    def as_dict(self) -> dict[str, object]:
        return {
            "cartan_type": self.cartan_type,
            "partition": self.partition,
            "q_value": self.q_value,
            "character": self.character,
            "source": self.source.as_dict(),
            "terms": [term.as_dict() for term in self.terms],
        }

    def json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)


def published_table(cartan_type, q_value: int, prefix: str = "s") -> PublishedMWTable:
    from modular_reduction.kls import KLSBasisSystem

    return KLSBasisSystem(cartan_type, prefix=prefix).published_table(q_value)


def basis_data(
    cartan_type,
    *,
    only_near_involutions: bool = False,
    q_value: int | None = None,
    prefix: str = "s",
) -> BasisDataset:
    from modular_reduction.kls import KLSBasisSystem

    return KLSBasisSystem(cartan_type, prefix=prefix).basis_data(
        only_near_involutions=only_near_involutions,
        q_value=q_value,
    )


def type_a_reduction(cartan_type, partition, q_value: int, prefix: str = "s") -> TypeAReductionResult:
    from modular_reduction.kls import KLSBasisSystem

    return KLSBasisSystem(cartan_type, prefix=prefix).reduction_data(partition, q_value)
