from __future__ import annotations

import argparse

from modular_reduction.kls import KLSBasisSystem


def _build_parser():
    parser = argparse.ArgumentParser(description="Sage-native modular reduction computations.")
    subparsers = parser.add_subparsers(dest="command", required=True)

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

    reduction_parser = subparsers.add_parser(
        "reduction",
        help="Compute the Type A modular reduction indexed by a partition.",
    )
    reduction_parser.add_argument("cartan_type", help="Cartan type such as A2 or A4.")
    reduction_parser.add_argument("q", type=int, help="The Frobenius power q.")
    reduction_parser.add_argument("partition", help="A partition such as 2,1,1.")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    system = KLSBasisSystem(args.cartan_type)

    if args.command == "mw":
        element = system.context.element_from_word(args.word)
        print(system.mw(element, args.q))
        return 0

    if args.command == "reduction":
        print(system.reduction(args.partition, args.q))
        return 0

    if args.format == "json":
        print(system.mw_json(args.q))
        return 0

    if args.format == "latex":
        print(system.mw_latex_table(args.q))
        return 0

    for row in system.mw_rows(args.q):
        print(f"{row.word}: {row.character}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
