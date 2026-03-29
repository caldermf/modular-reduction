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
from modular_reduction import KLSBasisSystem

system = KLSBasisSystem("A2")
w = system.context.element_from_word("s1")

print(system.mw(w, 11))
print(system.mw_table(11))
print(system.reduction((2, 1), 11))
print(system.mw_latex_table(11))
```

There is also a small CLI:

```bash
modred mw A2 11 s1
modred table B2 29
modred table B3 29 --format latex
modred reduction A3 29 2,1,1
```

## Tests

Run the default test suite with Sage:

```bash
sage -python -m pytest
```

The expensive paper-table and duality regressions are marked `slow` and skipped by default. Run them explicitly with:

```bash
sage -python -m pytest -m slow
```
