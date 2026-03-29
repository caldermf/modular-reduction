from __future__ import annotations

import json
import re
from dataclasses import dataclass


_CHARACTER_PATTERN = re.compile(r"[A-Z][0-9]*\(([^)]*)\)")
_SIMPLE_REFLECTION_PATTERN = re.compile(r"s(\d+)")


def word_to_latex(word: str) -> str:
    if word == "1":
        return "1"
    return _SIMPLE_REFLECTION_PATTERN.sub(r"s_{\1}", word).replace("*", "")


def character_to_paper_string(character) -> str:
    return _CHARACTER_PATTERN.sub(r"V_{\1}", str(character))


@dataclass(frozen=True)
class MWTableRow:
    word: str
    character: str
    latex_word: str
    latex_character: str

    def as_dict(self) -> dict[str, str]:
        return {
            "word": self.word,
            "character": self.character,
            "latex_word": self.latex_word,
            "latex_character": self.latex_character,
        }


def mw_rows(table: dict) -> tuple[MWTableRow, ...]:
    rows = []
    for element, character in table.items():
        word = str(element)
        rows.append(
            MWTableRow(
                word=word,
                character=character_to_paper_string(character),
                latex_word=word_to_latex(word),
                latex_character=character_to_paper_string(character),
            )
        )
    return tuple(rows)


def mw_json(table: dict) -> str:
    return json.dumps([row.as_dict() for row in mw_rows(table)], indent=2)


def mw_latex_table(cartan_type: tuple[str, int], table: dict) -> str:
    family, rank = cartan_type
    header = f"Type ${family}_{rank}$"
    rows = mw_rows(table)

    lines = [
        r"\begin{tabular}{|r|l|}",
        r"\hline",
        rf"\multicolumn{{2}}{{||c||}}{{{header}}}\\",
        r"\hline $w$ & $M_w$\\",
        r"\hline",
    ]
    for row in rows:
        lines.append(rf"${row.latex_word}$ & ${row.latex_character}$ \\")
    lines.extend([r"\hline", r"\end{tabular}"])
    return "\n".join(lines)
