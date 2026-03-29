# modular-reduction

`modular-reduction` is a research package in Python & Sage designed as a software companion to the paper

[_Modular reduction of complex representations of finite reductive groups_](https://arxiv.org/abs/2502.09605)   
by Roman Bezrukavnikov, Michael Finkelberg, David Kazhdan, and Calder Morton-Ferguson.

It allows for the computation of the Kazhdan-Lusztig-Steinberg basis on `C[T]`, its pseudo-dual and true dual bases, the virtual characters `M_w` from the paper, and modular reduction of irreducible unipotent representations in Type `A` directly from partitions.

The package may be used to:

- reproduce and extend the published `M_w` tables in our paper
- compute explicitly the basis elements `f_w`, `f^w`, and `f_w^*` in any Cartan type
- reproduce the paper’s computations of modular reductions of irreps via a clean Python API
- conduct other experiments with the KLS basis to build on the results of our paper

## What This Package Computes

For a Weyl group `W` of a chosen Cartan type, the package computes:

- the Kazhdan-Lusztig-Steinberg basis `f_w`
- the pseudo-dual basis `f^w`
- the true dual basis `f_w^*` with respect to the Weyl-character pairing on `C[T]` over `C[T]^W`
- Duflo involutions and Kazhdan-Lusztig left-cell data
- the virtual characters
  `M_w = < [q]^* f_{w_0 d}, f^*_{w_0 w} >`
  from the paper
- in Type `A`, the modular reduction attached to a partition by summing the relevant `M_w`

## Relationship to the Paper

The paper proves that Lusztig’s main conjectural formula for Brauer reduction of irreducible unipotent representations is correct in the sense that one can define explicit virtual characters `M_w` and write the Brauer reduction as

`underline(rho) = sum_w (rho : R_{alpha_w}) M_w`

over near involutions `w`.

This package implements the explicit objects appearing in that theorem:

- the basis `f_w`
- the pairing on `C[T]`
- the true dual basis `f_w^*`
- the Duflo involution attached to a left cell
- the paper’s definition of `M_w`

It also reproduces the computational phenomena emphasized in the paper:

- agreement with Lusztig’s original low-rank examples
- the distinction between the pseudo-dual basis `f^w` and the true dual basis `f_w^*`
- the resulting failure in general of some additional properties Lusztig had hoped the `M_w` might satisfy
- the Type `A_4` counterexample where `f^w` and `f_w^*` diverge

So, in a practical sense, this repository is the computational realization of the paper’s construction and of its resolution of Lusztig’s modular-reduction formula. The package also allows for the comparison of the actual `M_w` from the theorem with the "pseudo-dual" substitute `pseudo_mw(...)` which enjoys extra symmetry and positivity properties. This matters in Type `A_4`, where the package reproduces the failure of the pseudo-dual to equal the true dual, a discrepancy which is highlighted in the paper.

## Installation

This package is Sage-native. The expected workflow is to install it inside a Sage environment:

```bash
sage -pip install -e .
```

For development and testing:

```bash
sage -pip install -e .[test]
```

The code relies on Sage for Weyl groups, Kazhdan-Lusztig polynomials, Weyl character rings, and related combinatorics.

## Quick Start In Python

```python
from modular_reduction import KLSBasisSystem

system = KLSBasisSystem("A2")
w = system.context.element_from_word("s1")

print(system.basis_element(w))
print(system.pseudo_dual_element(w))
print(system.dual_basis_element(w))
print(system.mw(w, 11))
```

If you want a structured table object like the ones in the paper:

```python
from modular_reduction import published_table

table = published_table("B3", 29)

print(table.rows[0].word)
print(table.rows[0].character)
print(table.source.provenance.paper_reference)
print(table.json())
```

If you want basis-level data suitable for inspection or export:

```python
from modular_reduction import basis_data

dataset = basis_data("B2", only_near_involutions=True, q_value=29)

for datum in dataset.data:
    print(datum.word, datum.preferred_representative, datum.as_dict().get("mw"))
```

If you want a Type `A` reduction directly from a partition:

```python
from modular_reduction import type_a_reduction

result = type_a_reduction("A3", (2, 1, 1), 29)

print(result.character)
for term in result.terms:
    print(term.word, term.character)
```

## Command-Line Interface

The package comes with a small CLI under `modred`.

Compute one `M_w`:

```bash
modred mw A2 11 s1
```

Export a full published table:

```bash
modred table B3 29
modred table B3 29 --format json
modred table B3 29 --format latex
modred table B3 29 --format json --provenance
```

Inspect basis data:

```bash
modred basis A2 --near --q 11
modred basis B2 --near --q 29 --format json
```

Compute a Type `A` reduction:

```bash
modred reduction A3 29 2,1,1
modred reduction A3 29 2,1,1 --format json
```

Inspect provenance and supported types:

```bash
modred provenance A4
modred supported
```

## Table Examples

For a small type like `A2`, the plain-text table mode outputs:

| `w` | `M_w` |
| --- | --- |
| `1` | `V_{0,0}` |
| `s1` | `V_{10,0}` |
| `s2` | `V_{0,10}` |
| `s1*s2*s1` | `V_{10,10}` |

The package also emits exact LaTeX table code. For example,

```bash
modred table A2 11 --format latex
```

produces

```tex
\begin{tabular}{|r|l|}
\hline
\multicolumn{2}{||c||}{Type $A_2$}\\
\hline $w$ & $M_w$\\
\hline
$1$ & $V_{0,0}$ \\
$s_{1}$ & $V_{10,0}$ \\
$s_{2}$ & $V_{0,10}$ \\
$s_{1}s_{2}s_{1}$ & $V_{10,10}$ \\
\hline
\end{tabular}
```

## Public API

The most important entry points are:

- `KLSBasisSystem(cartan_type)`
- `published_table(cartan_type, q_value)`
- `basis_data(cartan_type, only_near_involutions=False, q_value=None)`
- `type_a_reduction(cartan_type, partition, q_value)`
- `provenance(cartan_type)`

The corresponding structured return types are:

- `PublishedMWTable`
- `BasisDataset`
- `TypeAReductionResult`
- `ProvenanceBundle`

These objects all have `as_dict()` methods, and the structured export objects also have `json()` helpers.

## Conventions

The package follows the paper’s conventions as closely as possible.

- `cartan_type="A4"` means the root system of type `A_4`.
- `mw(...)` is the paper’s `M_w`.
- `pseudo_mw(...)` is the alternative construction using the pseudo-dual instead of the honest dual basis.
- outputs are displayed in the paper’s Weyl-module notation, such as `V_{28,0,28}`.
- Type `A_n` reductions use partitions of `n+1`, matching the `SL(n+1)` convention in the paper.

The code accepts any integer `q`, but mathematically it is intended for the situation treated in the paper: `q` a power of a good prime.

## Supported and Verified Computations

The current regression suite verifies published `M_w` tables for:

- `A1`
- `A2`
- `A3`
- `B2`
- `G2`
- `B3`
- `C3`
- `A4`
- `D4`

In addition, the package includes:

- the `A4` dual-versus-pseudo-dual regression from the paper
- Type `A` partition-based reduction
- structured table export in plain text, JSON, and LaTeX

The package is capable of computing beyond these cases, but the list above is what is currently locked down by tests and provenance metadata.

## Example Scripts

Small runnable examples live in [`examples/`](examples):

- `examples/basic_usage.py`
- `examples/type_a_reduction.py`
- `examples/provenance_report.py`

Run them inside Sage, for example:

```bash
sage -python examples/basic_usage.py
```

## Relationship Between `f^w` And `f_w^*`

The pseudo-dual basis `f^w` is easy to write down explicitly, but it is not in general the true dual basis for the Weyl-character pairing. In small types these can agree on the associated graded pieces, and this is exactly why Lusztig’s original low-rank examples display extra symmetry. In larger types, especially `A4`, the difference becomes genuine and changes the resulting `M_w`.

If you are using this package for research, the safest rule is:

- use `dual_basis_element(...)` and `mw(...)` for actual computations
- use `pseudo_dual_element(...)` and `pseudo_mw(...)` only when you intentionally want to study this discrepancy

## Type `A` Reduction

For Type `A`, the package exposes a direct reduction API indexed by partitions. This reflects the paper’s Type `A` formulation, where the relevant summation runs over involutions in the two-sided cell corresponding to the partition.

For example, in type `A2`:

```python
from modular_reduction import KLSBasisSystem

system = KLSBasisSystem("A2")
print(system.reduction((2, 1), 11))
```

The structured API also tells you which `M_w` terms contributed:

```python
from modular_reduction import type_a_reduction

result = type_a_reduction("A2", (2, 1), 11)
print(result.character)
print([term.word for term in result.terms])
```

At the moment, this is the package’s direct high-level API for modular reduction of unipotent representations. For general types, computing the full reduction of an arbitrary unipotent representation still requires the relevant coefficients in Lusztig’s formula, which we have not yet implemented here.

## Development And Tests

Run the default test suite with Sage:

```bash
sage -python -m pytest
```

Run the slower paper-table and duality tests:

```bash
sage -python -m pytest -m slow
```

The test suite checks:

- low-rank tables from the paper
- `B3`, `C3`, and selected `D4` rows
- the `A4` dual/pseudo-dual discrepancy
- structured API/CLI behavior

## Repository Structure

The main pieces are:

- `src/modular_reduction/` for the package
- `tests/` for test coverage
- `examples/` for runnable usage examples
- `README.md`, `pyproject.toml` for package metadata
