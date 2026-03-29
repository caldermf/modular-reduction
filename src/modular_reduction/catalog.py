from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ProvenanceRecord:
    kind: str
    summary: str
    paper_reference: str
    notebook_path: str | None = None
    note: str | None = None
    verified_by_tests: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "summary": self.summary,
            "paper_reference": self.paper_reference,
            "notebook_path": self.notebook_path,
            "note": self.note,
            "verified_by_tests": self.verified_by_tests,
        }


@dataclass(frozen=True)
class CuratedRepresentativeSource:
    cartan_type: tuple[str, int]
    representatives: Mapping[str, str]
    provenance: ProvenanceRecord

    def as_dict(self) -> dict[str, object]:
        return {
            "cartan_type": self.cartan_type,
            "representatives": dict(self.representatives),
            "provenance": self.provenance.as_dict(),
        }


@dataclass(frozen=True)
class PublishedTableSource:
    cartan_type: tuple[str, int]
    provenance: ProvenanceRecord

    def as_dict(self) -> dict[str, object]:
        return {
            "cartan_type": self.cartan_type,
            "provenance": self.provenance.as_dict(),
        }


CURATED_LEFT_CELL_SOURCES: dict[tuple[str, int], CuratedRepresentativeSource] = {
    ("B", 2): CuratedRepresentativeSource(
        cartan_type=("B", 2),
        representatives={
            "s1*s2*s1": "s1",
            "s2*s1*s2": "s2",
        },
        provenance=ProvenanceRecord(
            kind="curated_left_cell_representatives",
            summary="Representative choices used in the B2 notebook computations to reproduce the published M_w table.",
            paper_reference="Main paper, combined small-rank table for Types A1/A2/B2/G2.",
            notebook_path="minimal_master_B2.ipynb",
            note="These representatives come from the historical research notebook lcell_dict and may differ from Sage's automatic Duflo involution choice.",
            verified_by_tests=True,
        ),
    ),
    ("G", 2): CuratedRepresentativeSource(
        cartan_type=("G", 2),
        representatives={
            "s2*s1*s2": "s2",
            "s2*s1*s2*s1*s2": "s2",
            "s1*s2*s1": "s1",
            "s1*s2*s1*s2*s1": "s1",
        },
        provenance=ProvenanceRecord(
            kind="curated_left_cell_representatives",
            summary="Representative choices used in the G2 notebook computations to reproduce the published M_w table.",
            paper_reference="Main paper, combined small-rank table for Types A1/A2/B2/G2.",
            notebook_path="minimal_master_G2.ipynb",
            note="As in B2, the historical notebook chooses preferred representatives within the relevant left cells rather than using the raw shifted elements.",
            verified_by_tests=True,
        ),
    ),
    ("B", 3): CuratedRepresentativeSource(
        cartan_type=("B", 3),
        representatives={
            "1": "1",
            "s1": "s1",
            "s1*s2*s3*s2*s1": "s1",
            "s2": "s2",
            "s2*s3*s2": "s2",
            "s3": "s3",
            "s3*s2*s3": "s3",
            "s3*s1": "s3*s1",
            "s2*s3*s1*s2": "s2*s3*s1*s2",
            "s3*s2*s3*s1*s2*s3": "s3*s2*s3*s1*s2*s3",
            "s1*s2*s1": "s1*s2*s1",
            "s3*s1*s2*s3*s1": "s3*s1*s2*s3*s1",
            "s2*s3*s1*s2*s3*s1*s2": "s2*s3*s1*s2*s3*s1*s2",
            "s3*s2*s3*s2": "s3*s2*s3*s2",
            "s3*s2*s3*s1*s2*s3*s1*s2": "s3*s2*s3*s2",
            "s3*s1*s2*s3*s2*s1": "s3*s1*s2*s3*s2*s1",
            "s3*s2*s3*s1*s2*s3*s2*s1": "s3*s1*s2*s3*s2*s1",
            "s1*s2*s3*s1*s2*s1": "s1*s2*s3*s1*s2*s1",
            "s2*s3*s1*s2*s3*s1*s2*s1": "s1*s2*s3*s1*s2*s1",
            "s3*s2*s3*s1*s2*s3*s1*s2*s1": "s3*s2*s3*s1*s2*s3*s1*s2*s1",
        },
        provenance=ProvenanceRecord(
            kind="curated_left_cell_representatives",
            summary="Representative choices used in the B3 notebook and paper table computations.",
            paper_reference="Main paper, Table B3 (tab:b3).",
            notebook_path="minimal_master_B3.ipynb",
            note="The historical notebook's lcell_dict uses hand-curated representatives within left cells; reproducing the paper table requires these choices instead of Sage's default Duflo picks.",
            verified_by_tests=True,
        ),
    ),
    ("C", 3): CuratedRepresentativeSource(
        cartan_type=("C", 3),
        representatives={
            "1": "1",
            "s1": "s1",
            "s1*s2*s3*s2*s1": "s1",
            "s2": "s2",
            "s2*s3*s2": "s2",
            "s3": "s3",
            "s3*s2*s3": "s3",
            "s3*s1": "s3*s1",
            "s2*s3*s1*s2": "s2*s3*s1*s2",
            "s3*s2*s3*s1*s2*s3": "s3*s2*s3*s1*s2*s3",
            "s1*s2*s1": "s1*s2*s1",
            "s3*s1*s2*s3*s1": "s3*s1*s2*s3*s1",
            "s2*s3*s1*s2*s3*s1*s2": "s2*s3*s1*s2*s3*s1*s2",
            "s3*s2*s3*s2": "s3*s2*s3*s2",
            "s3*s2*s3*s1*s2*s3*s1*s2": "s3*s2*s3*s2",
            "s3*s1*s2*s3*s2*s1": "s3*s1*s2*s3*s2*s1",
            "s3*s2*s3*s1*s2*s3*s2*s1": "s3*s1*s2*s3*s2*s1",
            "s1*s2*s3*s1*s2*s1": "s1*s2*s3*s1*s2*s1",
            "s2*s3*s1*s2*s3*s1*s2*s1": "s1*s2*s3*s1*s2*s1",
            "s3*s2*s3*s1*s2*s3*s1*s2*s1": "s3*s2*s3*s1*s2*s3*s1*s2*s1",
        },
        provenance=ProvenanceRecord(
            kind="curated_left_cell_representatives",
            summary="Representative choices used in the C3 notebook and paper table computations.",
            paper_reference="Main paper, Table C3 (tab:c3).",
            notebook_path="minimal_master_C3.ipynb",
            note="As in B3, these left-cell representatives come from the historical notebook lcell_dict rather than a purely automatic Sage rule.",
            verified_by_tests=True,
        ),
    ),
    ("D", 4): CuratedRepresentativeSource(
        cartan_type=("D", 4),
        representatives={
            "s2*s3*s1*s2*s4*s2*s3*s1*s2": "s2*s4*s3*s1*s2",
            "s3*s1*s2*s4*s1*s2*s3*s2*s1": "s1*s2*s3*s2*s1",
            "s4*s2*s3*s1*s2*s4*s1*s2*s3": "s3*s2*s4*s2*s3",
            "s4*s2*s3*s1*s2*s4*s3*s2*s1": "s1*s2*s4*s2*s1",
            "s3*s1*s2*s4*s2*s3*s1": "s4*s3*s1",
            "s1*s2*s4*s3*s1*s2*s1": "s1*s2*s1",
            "s3*s2*s4*s1*s2*s3*s2": "s2*s3*s2",
            "s4*s2*s3*s1*s2*s4*s2": "s2*s4*s2",
        },
        provenance=ProvenanceRecord(
            kind="curated_left_cell_representatives",
            summary="Representative choices used in the D4 notebook computations behind the published D4 table.",
            paper_reference="Main paper, Table D4 (tab:d4).",
            notebook_path="minimal_master_D4.ipynb",
            note="Only the exceptional left cells needed manual representative overrides in the historical notebook; all other involutions default to themselves.",
            verified_by_tests=True,
        ),
    ),
}

CURATED_LEFT_CELL_REPRESENTATIVE_MAPS: dict[tuple[str, int], Mapping[str, str]] = {
    cartan_type: source.representatives for cartan_type, source in CURATED_LEFT_CELL_SOURCES.items()
}

PUBLISHED_TABLE_SOURCES: dict[tuple[str, int], PublishedTableSource] = {
    ("A", 1): PublishedTableSource(
        cartan_type=("A", 1),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published A1 M_w table.",
            paper_reference="Main paper, combined small-rank table for Types A1/A2/B2/G2.",
            notebook_path="minimal_master_A1.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("A", 2): PublishedTableSource(
        cartan_type=("A", 2),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published A2 M_w table.",
            paper_reference="Main paper, combined small-rank table for Types A1/A2/B2/G2.",
            notebook_path="minimal_master_A2.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("B", 2): PublishedTableSource(
        cartan_type=("B", 2),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published B2 M_w table.",
            paper_reference="Main paper, combined small-rank table for Types A1/A2/B2/G2.",
            notebook_path="minimal_master_B2.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("G", 2): PublishedTableSource(
        cartan_type=("G", 2),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published G2 M_w table.",
            paper_reference="Main paper, combined small-rank table for Types A1/A2/B2/G2.",
            notebook_path="minimal_master_G2.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("A", 3): PublishedTableSource(
        cartan_type=("A", 3),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published A3 M_w table.",
            paper_reference="Main paper, Table A3 (tab:a3positivity).",
            notebook_path="minimal_master_A3.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("B", 3): PublishedTableSource(
        cartan_type=("B", 3),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published B3 M_w table.",
            paper_reference="Main paper, Table B3 (tab:b3).",
            notebook_path="minimal_master_B3.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("C", 3): PublishedTableSource(
        cartan_type=("C", 3),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published C3 M_w table.",
            paper_reference="Main paper, Table C3 (tab:c3).",
            notebook_path="minimal_master_C3.ipynb",
            verified_by_tests=True,
        ),
    ),
    ("A", 4): PublishedTableSource(
        cartan_type=("A", 4),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published A4 M_w table.",
            paper_reference="Main paper, Table A4 (tab:a4).",
            notebook_path="dual-basis-A4.ipynb",
            note="The A4 table is where the pseudo-dual and true dual diverge; the package's slow duality test is anchored here and traces back to the historical dual-basis-A4 notebook.",
            verified_by_tests=True,
        ),
    ),
    ("D", 4): PublishedTableSource(
        cartan_type=("D", 4),
        provenance=ProvenanceRecord(
            kind="published_mw_table",
            summary="Published D4 M_w table.",
            paper_reference="Main paper, Table D4 (tab:d4).",
            notebook_path="minimal_master_D4.ipynb",
            verified_by_tests=True,
        ),
    ),
}

TYPE_A_REDUCTION_SOURCE = ProvenanceRecord(
    kind="type_a_reduction",
    summary="Type A Brauer reduction obtained by summing M_w over involutions in the two-sided cell indexed by a partition.",
    paper_reference="Main paper, Type A corollary and the later Type A remark on unipotent representations.",
    notebook_path="A3_dual_and_sups.ipynb",
    note="The package identifies the two-sided cell of a partition through Robinson-Schensted shape and then sums the corresponding published M_w values, following the construction first explored in the historical A3_dual_and_sups notebook.",
    verified_by_tests=True,
)


def get_curated_representative_source(cartan_type) -> CuratedRepresentativeSource | None:
    return CURATED_LEFT_CELL_SOURCES.get(tuple(cartan_type))


def get_published_table_source(cartan_type) -> PublishedTableSource | None:
    return PUBLISHED_TABLE_SOURCES.get(tuple(cartan_type))


def get_type_a_reduction_source() -> ProvenanceRecord:
    return TYPE_A_REDUCTION_SOURCE


def published_cartan_types() -> tuple[tuple[str, int], ...]:
    return tuple(sorted(PUBLISHED_TABLE_SOURCES))


def curated_representative_cartan_types() -> tuple[tuple[str, int], ...]:
    return tuple(sorted(CURATED_LEFT_CELL_SOURCES))
