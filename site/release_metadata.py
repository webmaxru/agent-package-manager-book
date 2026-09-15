"""Shared, fail-closed metadata checks for book builds and content releases."""
from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

EDITION_PATTERN = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
APM_PATTERN = EDITION_PATTERN + r"\.(?:0|[1-9][0-9]*)"
SECTION_RE = re.compile(r"^##\s+\[([^\]]+)\].*$", re.MULTILINE)
HEADER_RE = re.compile(
    rf"##\s+\[({EDITION_PATTERN})\]\s+(?:-|\u2014)\s+(\d{{4}}-\d{{2}}-\d{{2}})"
)


class ReleaseError(ValueError):
    """A release input is missing, inconsistent, or unsafe to publish."""


@dataclass(frozen=True)
class Edition:
    version: str
    date: str
    apm_version: str


@dataclass(frozen=True)
class ChangelogEntry:
    version: str
    date: str
    notes: str


def version_number(value: Any, *, apm: bool = False) -> str:
    pattern = APM_PATTERN if apm else EDITION_PATTERN
    label = "APM version (X.Y.Z)" if apm else "content edition (X.Y)"
    if not isinstance(value, str) or not re.fullmatch(pattern, value):
        raise ReleaseError(f"Expected a quoted {label}, got {value!r}.")
    return value


def version_tuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def iso_date(value: Any, location: str) -> str:
    if type(value) is datetime.date:
        return value.isoformat()
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return datetime.date.fromisoformat(value).isoformat()
        except ValueError:
            pass
    raise ReleaseError(f"{location}: expected a valid YYYY-MM-DD date, got {value!r}.")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ReleaseError(f"Cannot read {path}: {error}") from error


def parse_metadata(text: str, location: str) -> dict[str, Any]:
    try:
        data = yaml.safe_load(text)
    except (yaml.YAMLError, ValueError) as error:
        raise ReleaseError(f"{location}: invalid YAML: {error}") from error
    if not isinstance(data, dict):
        raise ReleaseError(f"{location}: expected a YAML mapping.")
    return data


def read_edition(path: Path) -> Edition:
    data = parse_metadata(read_text(path), str(path))
    try:
        return Edition(
            version_number(data.get("version")),
            iso_date(data.get("date"), str(path)),
            version_number(data.get("apm_version"), apm=True),
        )
    except ReleaseError as error:
        raise ReleaseError(f"{path}: {error}") from error


def read_changelog(path: Path) -> list[ChangelogEntry]:
    text = read_text(path)
    sections = list(SECTION_RE.finditer(text))
    entries: list[ChangelogEntry] = []
    seen: set[str] = set()
    for index, section in enumerate(sections):
        if section.group(1) == "Unreleased":
            continue
        header = HEADER_RE.fullmatch(section.group(0).strip())
        if header is None:
            raise ReleaseError(
                f"{path}: malformed edition heading {section.group(0)!r}; "
                "expected '## [X.Y] - YYYY-MM-DD'."
            )
        version, date = header.groups()
        if version in seen:
            raise ReleaseError(f"{path}: duplicate changelog entry for v{version}.")
        seen.add(version)
        iso_date(date, str(path))
        end = sections[index + 1].start() if index + 1 < len(sections) else len(text)
        notes = text[section.start():end].strip() + "\n"
        body = re.sub(r"<!--.*?-->", "", notes.split("\n", 1)[-1], flags=re.DOTALL)
        if not any(line.strip() and not line.lstrip().startswith("#") for line in body.splitlines()):
            raise ReleaseError(f"{path}: changelog entry for v{version} has no release notes.")
        entries.append(ChangelogEntry(version, date, notes))
    if not entries:
        raise ReleaseError(f"{path}: no content-edition changelog entries found.")
    return entries


def release_notes(version: str, path: Path) -> str:
    version = version_number(version.removeprefix("v"))
    for entry in read_changelog(path):
        if entry.version == version:
            return entry.notes
    raise ReleaseError(f"{path}: no changelog entry for v{version}. Add it before releasing.")


def validate_metadata(root: Path) -> tuple[Edition, list[ChangelogEntry]]:
    edition = read_edition(root / "content" / "version.yml")
    entries = read_changelog(root / "content" / "CHANGELOG.md")
    if entries[0].version != edition.version:
        raise ReleaseError("The first released CHANGELOG entry must match content/version.yml.")
    if entries[0].date != edition.date:
        raise ReleaseError("The edition date and its CHANGELOG heading date must match.")
    versions = [version_tuple(entry.version) for entry in entries]
    if versions != sorted(versions, reverse=True):
        raise ReleaseError("CHANGELOG editions must be ordered newest first.")
    return edition, entries
