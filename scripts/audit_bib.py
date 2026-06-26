#!/usr/bin/env python3
"""Audit a BibTeX file for source-centric genealogy maintenance.

The parser is intentionally dependency-free and conservative. It identifies
structural problems and candidate duplicate sources, but never merges entries.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ENTRY_START_RE = re.compile(r"@([A-Za-z]+)\s*([({])", re.MULTILINE)
FIELD_START_RE = re.compile(r"([A-Za-z][A-Za-z0-9_-]*)\s*=", re.MULTILINE)
FAMILYSEARCH_IG_RE = re.compile(
    r"(?:image\s+group\s+number|digital\s+folder\s+number|dgs(?:\s+number)?)"
    r"\s*[:#]?\s*([0-9][0-9_ -]{5,})",
    re.IGNORECASE,
)
ANCESTRY_COLLECTION_RE = re.compile(r"/collections/(\d+)(?:/|$)", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"(?:X{3,}|example\.com|TODO|TBD)", re.IGNORECASE)


@dataclass
class Entry:
    entry_type: str
    key: str
    fields: dict[str, str]
    duplicate_fields: list[str]
    start_line: int
    raw: str


@dataclass
class Audit:
    entries: list[Entry] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def strip_outer(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    changed = True
    while changed and len(value) >= 2:
        changed = False
        if value[0] == "{" and value[-1] == "}":
            depth = 0
            balanced = True
            for index, char in enumerate(value):
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0 and index != len(value) - 1:
                        balanced = False
                        break
            if balanced and depth == 0:
                value = value[1:-1].strip()
                changed = True
        elif value[0] == '"' and value[-1] == '"':
            value = value[1:-1].strip()
            changed = True
    return value


def normalized_text(value: str) -> str:
    value = strip_outer(value)
    value = re.sub(r"\\[A-Za-z]+\*?(?:\[[^]]*\])?", " ", value)
    value = value.replace("{", "").replace("}", "")
    value = value.replace("~", " ")
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    start = 0
    brace_depth = 0
    paren_depth = 0
    in_quote = False
    escaped = False

    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"' and brace_depth == 0:
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth -= 1
        elif char == delimiter and brace_depth == 0 and paren_depth == 0:
            parts.append(text[start:index])
            start = index + 1

    parts.append(text[start:])
    return parts


def parse_fields(body: str) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    duplicates: list[str] = []
    for part in split_top_level(body):
        part = part.strip()
        if not part:
            continue
        match = FIELD_START_RE.match(part)
        if not match:
            continue
        name = match.group(1).casefold()
        value = part[match.end():].strip()
        if name in fields:
            duplicates.append(name)
        else:
            fields[name] = strip_outer(value)
    return fields, duplicates


def parse_bibtex(text: str) -> Audit:
    audit = Audit()
    position = 0

    while True:
        match = ENTRY_START_RE.search(text, position)
        if not match:
            break

        entry_type = match.group(1).casefold()
        opener = match.group(2)
        closer = "}" if opener == "{" else ")"
        content_start = match.end()
        depth = 1
        in_quote = False
        escaped = False
        index = content_start

        while index < len(text) and depth:
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"' and depth == 1:
                in_quote = not in_quote
            elif not in_quote:
                if char == opener:
                    depth += 1
                elif char == closer:
                    depth -= 1
            index += 1

        start_line = line_number(text, match.start())
        if depth:
            audit.parse_errors.append(
                f"Line {start_line}: unterminated @{entry_type} entry"
            )
            break

        raw = text[match.start():index]
        content = text[content_start:index - 1]
        first_comma = None
        brace_depth = 0
        in_quote = False
        escaped = False
        for relative_index, char in enumerate(content):
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"' and brace_depth == 0:
                in_quote = not in_quote
                continue
            if in_quote:
                continue
            if char == "{":
                brace_depth += 1
            elif char == "}":
                brace_depth -= 1
            elif char == "," and brace_depth == 0:
                first_comma = relative_index
                break

        if first_comma is None:
            audit.parse_errors.append(
                f"Line {start_line}: entry has no key/field separator"
            )
            position = index
            continue

        key = content[:first_comma].strip()
        body = content[first_comma + 1:]
        fields, duplicate_fields = parse_fields(body)
        audit.entries.append(
            Entry(entry_type, key, fields, duplicate_fields, start_line, raw)
        )
        position = index

    return audit


def group_entries(
    entries: Iterable[Entry], key_function
) -> list[tuple[str, list[Entry]]]:
    groups: dict[str, list[Entry]] = defaultdict(list)
    for entry in entries:
        candidate = key_function(entry)
        if candidate:
            groups[candidate].append(entry)
    return sorted(
        ((key, values) for key, values in groups.items() if len(values) > 1),
        key=lambda item: (-len(item[1]), item[0]),
    )


def familysearch_ids(entry: Entry) -> set[str]:
    haystack = " ".join(entry.fields.values())
    identifiers = set()
    for match in FAMILYSEARCH_IG_RE.finditer(haystack):
        digits = re.sub(r"\D", "", match.group(1))
        if len(digits) >= 6:
            identifiers.add(digits)
    return identifiers


def ancestry_collection_ids(entry: Entry) -> set[str]:
    identifiers = set()
    for value in entry.fields.values():
        identifiers.update(ANCESTRY_COLLECTION_RE.findall(value))
    return identifiers


def source_identity(entry: Entry) -> str | None:
    title = normalized_text(entry.fields.get("title", ""))
    if not title:
        return None
    container = normalized_text(
        entry.fields.get("booktitle", "")
        or entry.fields.get("journaltitle", "")
        or entry.fields.get("journal", "")
        or entry.fields.get("collection", "")
    )
    author = normalized_text(
        entry.fields.get("author", "")
        or entry.fields.get("editor", "")
        or entry.fields.get("organization", "")
    )
    year = normalized_text(entry.fields.get("year", ""))
    return " | ".join((title, container, author, year))


def exact_title(entry: Entry) -> str | None:
    title = normalized_text(entry.fields.get("title", ""))
    return title or None


def exact_url(entry: Entry) -> str | None:
    url = strip_outer(entry.fields.get("url", "")).strip()
    return url.casefold() or None


def summarize_group(label: str, groups: list[tuple[str, list[Entry]]]) -> list[dict]:
    output = []
    for identity, entries in groups:
        output.append(
            {
                "basis": label,
                "identity": identity,
                "keys": [entry.key for entry in entries],
                "lines": [entry.start_line for entry in entries],
            }
        )
    return output


def build_report(audit: Audit) -> dict:
    entries = audit.entries
    keys: dict[str, list[Entry]] = defaultdict(list)
    for entry in entries:
        keys[entry.key].append(entry)

    duplicate_keys = {
        key: [entry.start_line for entry in values]
        for key, values in keys.items()
        if len(values) > 1
    }
    invalid_keys = [
        {"key": entry.key, "line": entry.start_line}
        for entry in entries
        if not KEY_RE.fullmatch(entry.key)
    ]
    missing_filename = [
        {"key": entry.key, "line": entry.start_line}
        for entry in entries
        if "filename" not in entry.fields
    ]
    filename_mismatches = [
        {
            "key": entry.key,
            "filename": entry.fields.get("filename", ""),
            "line": entry.start_line,
        }
        for entry in entries
        if "filename" in entry.fields
        and strip_outer(entry.fields["filename"]) != entry.key
    ]
    duplicate_fields = [
        {"key": entry.key, "fields": entry.duplicate_fields, "line": entry.start_line}
        for entry in entries
        if entry.duplicate_fields
    ]

    missing_metadata = []
    placeholders = []
    for entry in entries:
        missing = []
        if not entry.fields.get("title"):
            missing.append("title")
        if entry.entry_type in {"book", "article", "inbook", "incollection"}:
            if not (entry.fields.get("author") or entry.fields.get("editor")):
                missing.append("author/editor")
            if not (entry.fields.get("year") or entry.fields.get("date")):
                missing.append("year/date")
        if entry.entry_type == "article" and not (
            entry.fields.get("journaltitle") or entry.fields.get("journal")
        ):
            missing.append("journal/journaltitle")
        if missing:
            missing_metadata.append(
                {"key": entry.key, "missing": missing, "line": entry.start_line}
            )
        if PLACEHOLDER_RE.search(entry.raw):
            placeholders.append({"key": entry.key, "line": entry.start_line})

    familysearch_groups: dict[str, list[Entry]] = defaultdict(list)
    ancestry_groups: dict[str, list[Entry]] = defaultdict(list)
    for entry in entries:
        for identifier in familysearch_ids(entry):
            familysearch_groups[identifier].append(entry)
        for identifier in ancestry_collection_ids(entry):
            ancestry_groups[identifier].append(entry)

    candidate_groups = []
    candidate_groups.extend(
        summarize_group("exact source identity", group_entries(entries, source_identity))
    )
    candidate_groups.extend(
        summarize_group("exact normalized title", group_entries(entries, exact_title))
    )
    candidate_groups.extend(
        summarize_group("exact URL", group_entries(entries, exact_url))
    )
    candidate_groups.extend(
        summarize_group(
            "FamilySearch image group number",
            sorted(
                (
                    (identity, values)
                    for identity, values in familysearch_groups.items()
                    if len(values) > 1
                ),
                key=lambda item: (-len(item[1]), item[0]),
            ),
        )
    )
    candidate_groups.extend(
        summarize_group(
            "Ancestry collection ID",
            sorted(
                (
                    (identity, values)
                    for identity, values in ancestry_groups.items()
                    if len(values) > 1
                ),
                key=lambda item: (-len(item[1]), item[0]),
            ),
        )
    )

    unique_candidates = {}
    for candidate in candidate_groups:
        signature = tuple(sorted(candidate["keys"]))
        record = unique_candidates.setdefault(
            signature,
            {
                "keys": list(signature),
                "lines": sorted(set(candidate["lines"])),
                "evidence": [],
            },
        )
        record["evidence"].append(
            {"basis": candidate["basis"], "identity": candidate["identity"]}
        )

    return {
        "original_entry_count": len(entries),
        "parse_errors": audit.parse_errors,
        "duplicate_keys": duplicate_keys,
        "invalid_keys": invalid_keys,
        "missing_filename": missing_filename,
        "filename_mismatches": filename_mismatches,
        "duplicate_fields": duplicate_fields,
        "missing_metadata": missing_metadata,
        "placeholders": placeholders,
        "candidate_duplicate_groups": sorted(
            unique_candidates.values(), key=lambda item: (-len(item["keys"]), item["keys"])
        ),
    }


def markdown_list(items: list[str], empty: str = "None detected.") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def render_markdown(report: dict) -> str:
    candidate_groups = report["candidate_duplicate_groups"]
    lines = [
        "# Lineage BibTeX Audit Report",
        "",
        "This report identifies mechanical problems and conservative duplicate candidates.",
        "Candidate groups require source review before any merge.",
        "",
        "## Summary",
        "",
        f"- Original entry count: **{report['original_entry_count']}**",
        f"- Duplicate key groups: **{len(report['duplicate_keys'])}**",
        f"- Invalid source-key formats: **{len(report['invalid_keys'])}**",
        f"- Entries missing `filename`: **{len(report['missing_filename'])}**",
        f"- `filename` mismatches: **{len(report['filename_mismatches'])}**",
        f"- Entries with duplicate fields: **{len(report['duplicate_fields'])}**",
        f"- Entries with missing core metadata: **{len(report['missing_metadata'])}**",
        f"- Placeholder values: **{len(report['placeholders'])}**",
        f"- Candidate duplicate groups: **{len(candidate_groups)}**",
        "",
        "## Parse errors",
        "",
        markdown_list(report["parse_errors"]),
        "",
        "## Duplicate keys",
        "",
        markdown_list(
            [f"`{key}` — lines {', '.join(map(str, line_numbers))}"
             for key, line_numbers in report["duplicate_keys"].items()]
        ),
        "",
        "## Invalid key formats",
        "",
        markdown_list(
            [f"`{item['key']}` — line {item['line']}" for item in report["invalid_keys"]]
        ),
        "",
        "## Missing or mismatched filename fields",
        "",
        "### Missing",
        "",
        markdown_list(
            [f"`{item['key']}` — line {item['line']}" for item in report["missing_filename"]]
        ),
        "",
        "### Mismatched",
        "",
        markdown_list(
            [f"`{item['key']}` has `{item['filename']}` — line {item['line']}"
             for item in report["filename_mismatches"]]
        ),
        "",
        "## Duplicate fields",
        "",
        markdown_list(
            [f"`{item['key']}` repeats {', '.join(f'`{name}`' for name in item['fields'])} — line {item['line']}"
             for item in report["duplicate_fields"]]
        ),
        "",
        "## Candidate duplicate sources",
        "",
    ]

    if not candidate_groups:
        lines.append("None detected mechanically.")
    else:
        for index, group in enumerate(candidate_groups, 1):
            lines.extend(
                [
                    f"### Candidate {index}",
                    "",
                    f"Keys: {', '.join(f'`{key}`' for key in group['keys'])}",
                    "",
                    "Evidence:",
                    "",
                ]
            )
            for evidence in group["evidence"]:
                lines.append(
                    f"- {evidence['basis']}: `{evidence['identity']}`"
                )
            lines.append("")

    lines.extend(
        [
            "## Missing core metadata",
            "",
            markdown_list(
                [f"`{item['key']}` lacks {', '.join(item['missing'])} — line {item['line']}"
                 for item in report["missing_metadata"]]
            ),
            "",
            "## Placeholder values",
            "",
            markdown_list(
                [f"`{item['key']}` — line {item['line']}" for item in report["placeholders"]]
            ),
            "",
            "## Consolidation status",
            "",
            "- Final entry count: pending source review",
            "- Duplicates merged: none by this audit",
            "- Entries needing manual review: candidate groups above",
            "- Possible citation problems: parse errors, placeholders, duplicate fields, and metadata gaps above",
            "",
        ]
    )
    return "\n".join(lines)


def write_migration_candidates(path: Path, report: dict) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["old_key", "proposed_new_key", "status", "evidence"])
        for index, group in enumerate(report["candidate_duplicate_groups"], 1):
            evidence = "; ".join(
                f"{item['basis']}: {item['identity']}" for item in group["evidence"]
            )
            for key in group["keys"]:
                writer.writerow([key, "", f"review-candidate-{index}", evidence])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bibfile", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--migration-candidates", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a nonzero status when structural or filename errors exist",
    )
    args = parser.parse_args()

    text = args.bibfile.read_text(encoding="utf-8")
    audit = parse_bibtex(text)
    report = build_report(audit)
    rendered = render_markdown(report)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if args.migration_candidates:
        args.migration_candidates.parent.mkdir(parents=True, exist_ok=True)
        write_migration_candidates(args.migration_candidates, report)

    if args.strict and any(
        (
            report["parse_errors"],
            report["duplicate_keys"],
            report["missing_filename"],
            report["filename_mismatches"],
        )
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
