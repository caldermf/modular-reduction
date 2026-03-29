# modular-reduction

Sage-native tools for computing the Kazhdan-Lusztig-Steinberg basis, its dual and pseudo-dual bases, the virtual characters `M_w` from the paper, and Type `A` modular reduction directly from partitions.

## Status

This repository is in the middle of being converted from research notebooks into a real installable package. The first package extraction now lives under `src/modular_reduction/` and already supports:

- Sage-backed Cartan type contexts
- programmatic Kazhdan-Lusztig left-cell computation through Sage
- Duflo involution selection from left cells
- computation of the KLS basis, pseudo-dual basis, true dual basis, and paper-consistent `M_w`
- Type `A` reduction from a partition/Young diagram
- plain, JSON, and LaTeX table export helpers
- regression tests for the small-rank cases `A1`, `A2`, and `B2`
- slow regression tests for the published `B3`, `C3`, and `D4` tables and the `A4` dual-vs-pseudo-dual discrepancy

## Installation

This is intentionally Sage-native. The expected workflow is to install it inside a Sage environment:

```bash
sage -pip install -e .
```

If you want faster Kazhdan-Lusztig cell computations, Sage's optional `coxeter3` support is recommended, but it is not required.

## Quick Start

```python
from modular_reduction import KLSBasisSystem, basis_data, published_table, type_a_reduction

system = KLSBasisSystem("A2")
w = system.context.element_from_word("s1")

print(system.mw(w, 11))
print(system.mw_table(11))
print(system.reduction((2, 1), 11))
print(system.mw_latex_table(11))

table = published_table("A2", 11)
print(table.rows[1].character)
print(table.source.provenance.paper_reference)

dataset = basis_data("B2", only_near_involutions=True, q_value=29)
print(dataset.representative_source.provenance.note)

reduction = type_a_reduction("A2", (2, 1), 11)
print(reduction.character)
print([term.word for term in reduction.terms])
```

There is also a small CLI:

```bash
modred mw A2 11 s1
modred table B2 29
modred table B3 29 --format latex
modred reduction A3 29 2,1,1
```

## Provenance

The package now carries explicit provenance metadata for the paper-facing computations:

- published `M_w` tables are tagged with the paper table reference and the notebook used to verify them
- curated left-cell representatives in `B2`, `B3`, `C3`, and `D4` are documented as notebook-derived overrides
- Type `A` reduction data records the paper section and notebook path behind the partition-based construction

This is meant to make it easy for researchers to move back and forth between the package, the paper, and the original exploratory notebooks.

## Tests

Run the default test suite with Sage:

```bash
sage -python -m pytest
```

The expensive paper-table and duality regressions are marked `slow` and skipped by default. Run them explicitly with:

```bash
sage -python -m pytest -m slow
```
