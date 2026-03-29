from __future__ import annotations

from sage.all import RSK


def normalize_partition(partition, size: int) -> tuple[int, ...]:
    if isinstance(partition, str):
        parts = tuple(int(part.strip()) for part in partition.split(",") if part.strip())
    else:
        parts = tuple(int(part) for part in partition)

    if not parts:
        raise ValueError("A partition must have at least one positive part.")
    if any(part <= 0 for part in parts):
        raise ValueError(f"Invalid partition {parts!r}: all parts must be positive.")
    if tuple(sorted(parts, reverse=True)) != parts:
        raise ValueError(f"Invalid partition {parts!r}: parts must be weakly decreasing.")
    if sum(parts) != size:
        raise ValueError(f"Partition {parts!r} must sum to {size}.")

    return parts


def element_shape(w) -> tuple[int, ...]:
    insertion_tableau, _ = RSK(w.to_permutation())
    return tuple(len(row) for row in insertion_tableau)


def cell_involutions(system, partition) -> tuple:
    if system.context.cartan_type[0] != "A":
        raise ValueError("Partition-indexed reduction is only implemented for Type A.")

    normalized = normalize_partition(partition, system.context.rank + 1)
    identity = system.context.identity

    return tuple(
        w
        for w in system.context.elements
        if w * w == identity and element_shape(w) == normalized
    )


def reduction(system, partition, q_value: int):
    total = 0
    for w in cell_involutions(system, partition):
        total += system.mw(w, q_value)
    return total
