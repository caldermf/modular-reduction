from __future__ import annotations

import argparse

from modular_reduction import curated_representative_cartan_types, published_cartan_types
from modular_reduction.kls import KLSBasisSystem


def _build_parser():
    parser = argparse.ArgumentParser(description="Sage-native modular reduction computations.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "supported",
        help="List the Cartan types with paper-table and curated representative support.",
    )

    mw_parser = subparsers.add_parser("mw", help="Compute M_w for one Weyl group element.")
    mw_parser.add_argument("cartan_type", help="Cartan type such as A2 or B3.")
    mw_parser.add_argument("q", type=int, help="The Frobenius power q.")
    mw_parser.add_argument("word", help="A Weyl group word such as 1 or s2*s1*s2.")

    table_parser = subparsers.add_parser("table", help="Compute M_w for all near involutions.")
    table_parser.add_argument("cartan_type", help="Cartan type such as A2 or B3.")
    table_parser.add_argument("q", type=int, help="The Frobenius power q.")
    table_parser.add_argument(
        "--format",
        choices=("plain", "latex", "json"),
        default="plain",
        help="Output format for the table.",
    )
    table_parser.add_argument(
        "--provenance",
        action="store_true",
        help="Include provenance metadata in plain or JSON output.",
    )

    basis_parser = subparsers.add_parser(
        "basis",
        help="Inspect basis, dual, and cell data for one type.",
    )
    basis_parser.add_argument("cartan_type", help="Cartan type such as A2 or B3.")
    basis_parser.add_argument(
        "--near",
        action="store_true",
        help="Restrict to near involutions.",
    )
    basis_parser.add_argument(
        "--q",
        type=int,
        default=None,
        help="If provided, also compute M_w values for near involutions.",
    )
    basis_parser.add_argument(
        "--format",
        choices=("plain", "json"),
        default="plain",
        help="Output format for the basis dataset.",
    )

    reduction_parser = subparsers.add_parser(
        "reduction",
        help="Compute the Type A modular reduction indexed by a partition.",
    )
    reduction_parser.add_argument("cartan_type", help="Cartan type such as A2 or A4.")
    reduction_parser.add_argument("q", type=int, help="The Frobenius power q.")
    reduction_parser.add_argument("partition", help="A partition such as 2,1,1.")
    reduction_parser.add_argument(
        "--format",
        choices=("plain", "json"),
        default="plain",
        help="Output format for the reduction result.",
    )

    provenance_parser = subparsers.add_parser(
        "provenance",
        help="Show the paper/notebook provenance for one Cartan type.",
    )
    provenance_parser.add_argument("cartan_type", help="Cartan type such as A2 or D4.")
    provenance_parser.add_argument(
        "--format",
        choices=("plain", "json"),
        default="plain",
        help="Output format for the provenance report.",
    )

    return parser


def _format_cartan_type(cartan_type) -> str:
    return f"{cartan_type[0]}{cartan_type[1]}"


def _print_supported() -> None:
    published = ", ".join(_format_cartan_type(ct) for ct in published_cartan_types())
    curated = ", ".join(_format_cartan_type(ct) for ct in curated_representative_cartan_types())
    print(f"Published paper tables: {published}")
    print(f"Curated left-cell representatives: {curated}")
    print("Type A reduction: available for every type A_n via partitions of n+1")


def _print_basis_dataset(dataset) -> None:
    for datum in dataset.data:
        pieces = [
            datum.word,
            f"descents={datum.right_descents}",
            f"near={datum.is_near_involution}",
            f"duflo={datum.duflo_involution}",
            f"representative={datum.preferred_representative}",
        ]
        if datum.type_a_shape is not None:
            pieces.append(f"shape={datum.type_a_shape}")
        if datum.mw_value is not None:
            pieces.append(f"M_w={datum.as_dict()['mw']}")
        print("; ".join(pieces))


def _print_provenance(report) -> None:
    print(f"Cartan type: {_format_cartan_type(report.cartan_type)}")
    if report.published_table is not None:
        provenance = report.published_table.provenance
        print(f"Published table: {provenance.paper_reference}")
        if provenance.notebook_path is not None:
            print(f"Published table notebook: {provenance.notebook_path}")
    if report.representative_source is not None:
        provenance = report.representative_source.provenance
        print(f"Curated representatives: {provenance.paper_reference}")
        if provenance.notebook_path is not None:
            print(f"Representative notebook: {provenance.notebook_path}")
    if report.type_a_reduction is not None:
        provenance = report.type_a_reduction
        print(f"Type A reduction: {provenance.paper_reference}")
        if provenance.notebook_path is not None:
            print(f"Type A reduction notebook: {provenance.notebook_path}")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "supported":
        _print_supported()
        return 0

    system = KLSBasisSystem(args.cartan_type)

    if args.command == "mw":
        element = system.context.element_from_word(args.word)
        print(system.mw(element, args.q))
        return 0

    if args.command == "basis":
        dataset = system.basis_data(only_near_involutions=args.near, q_value=args.q)
        if args.format == "json":
            print(dataset.json())
            return 0
        _print_basis_dataset(dataset)
        return 0

    if args.command == "reduction":
        reduction = system.reduction_data(args.partition, args.q)
        if args.format == "json":
            print(reduction.json())
            return 0
        print(reduction.character)
        for term in reduction.terms:
            print(f"  {term.word}: {term.character}")
        return 0

    if args.command == "provenance":
        report = system.provenance()
        if args.format == "json":
            print(report.json())
            return 0
        _print_provenance(report)
        return 0

    if args.format == "json":
        table = system.published_table(args.q)
        if args.provenance:
            print(table.json())
        else:
            print(system.mw_json(args.q))
        return 0

    if args.format == "latex":
        print(system.mw_latex_table(args.q))
        return 0

    for row in system.mw_rows(args.q):
        print(f"{row.word}: {row.character}")
    if args.provenance:
        print("")
        _print_provenance(system.provenance())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
