"""Writing-style rules: mechanical tells are errors, AI vocabulary is a warning.

Decision: ADR-0005 (writing style and its enforcement).
Source list: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
"""

from __future__ import annotations

import re
from pathlib import Path

from .report import Violation

EM_DASH = chr(0x2014)
CURLY_QUOTES = "".join(map(chr, (0x2018, 0x2019, 0x201C, 0x201D)))

# Chat-tool citation residue: never legitimate in this repository. Each token is split across
# string pieces so this source file does not itself contain the artifacts it detects.
_ARTIFACT_TOKENS = (
    "content" "Reference", "oai" "cite", "oai" "_citation", "attributable" "Index",
    "grok" "_card", "grok" "_render", "ppl-ai" "-file-upload", "attached" "_file", ":::" "writing",
)
_ARTIFACT = re.compile(
    "|".join(re.escape(t) for t in _ARTIFACT_TOKENS) + r"|turn\d+search\d+|\[cite:\s*\d"
)

# Warned, not blocked: these words have legitimate uses, so context decides.
AI_VOCABULARY = (
    "additionally", "boasts", "bolstered", "crucial", "deeply rooted", "delve", "delves", "delving",
    "emphasizing", "evolving landscape", "fostering", "garner", "groundbreaking", "highlighting",
    "in conclusion", "in the heart of", "indelible mark", "interplay", "intricate", "intricacies",
    "is a testament", "it is important to note", "it's important to note", "meticulous",
    "meticulously", "nestled", "not only", "pivotal", "renowned", "serves as", "showcase",
    "showcases", "showcasing", "stands as", "tapestry", "testament", "underscore", "underscores",
    "valuable insights", "vibrant", "i hope this helps", "certainly!", "let me explain",
    "as of my knowledge cutoff",
)
_VOCAB = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in AI_VOCABULARY) + r")(?![\w-])", re.I)


def check_style(root: Path, files: list[str]) -> list[Violation]:
    v: list[Violation] = []
    for rel in files:
        try:
            lines = (root / rel).read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        markdown = rel.endswith(".md")
        for n, line in enumerate(lines, start=1):
            if EM_DASH in line:
                v.append(Violation(rel, n, "STYLE-EM-DASH",
                                   "em dash; use a comma, colon, period, parentheses or a hyphen"))
            if any(q in line for q in CURLY_QUOTES):
                v.append(Violation(rel, n, "STYLE-CURLY-QUOTE", "curly quote; use straight quotes"))
            m = _ARTIFACT.search(line)
            if m:
                v.append(Violation(rel, n, "STYLE-AI-ARTIFACT", f"chat-tool artifact {m.group(0)!r}"))
            if markdown:
                for w in _VOCAB.finditer(line):
                    v.append(Violation(rel, n, "STYLE-AI-VOCABULARY",
                                       f"{w.group(0)!r} is on the AI-vocabulary list (ADR-0005); reword if it adds nothing"))
    return v
