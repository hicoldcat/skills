from __future__ import annotations

import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
REQUIRED_SECTIONS = ["## Triggers", "## Examples"]
CODE_SPAN_RE = re.compile(r"`([^`]+)`")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Missing YAML frontmatter delimited by ---")

    raw = match.group(1)
    body = text[match.end() :]
    data: dict[str, str] = {}

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if ":" not in stripped:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(('"', "'")) and value.endswith(('"', "'")):
            value = value[1:-1]
        data[key] = value

    return data, body


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter, body = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_md}: {exc}"]

    is_template = skill_dir.name == "_template"

    missing = ALLOWED_FRONTMATTER_KEYS - set(frontmatter)
    extra = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS

    if missing:
        errors.append(f"{skill_md}: missing frontmatter keys: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{skill_md}: unsupported frontmatter keys: {', '.join(sorted(extra))}")

    expected_name = skill_dir.name
    actual_name = frontmatter.get("name", "")
    if actual_name and actual_name != expected_name and not is_template:
        errors.append(f"{skill_md}: frontmatter name '{actual_name}' must match folder name '{expected_name}'")

    if actual_name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", actual_name) and not is_template:
        errors.append(f"{skill_md}: name must be lowercase kebab-case")

    description = frontmatter.get("description", "")
    if description and len(description) < 40 and not is_template:
        errors.append(f"{skill_md}: description is too short to be a good trigger")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{skill_md}: missing required section '{section}'")

    for code_span in CODE_SPAN_RE.findall(body):
        for prefix in ("scripts/", "references/", "assets/"):
            if not code_span.startswith(prefix):
                continue
            if is_template:
                continue
            ref_path = skill_dir / code_span
            if not ref_path.exists():
                errors.append(f"{skill_md}: referenced path not found: {code_span}")

    meta_file = skill_dir / "_meta.json"
    if meta_file.exists():
        errors.append(f"{skill_dir}: _meta.json should not exist in Claude Code skill format")

    return errors


def collect_skill_dirs(path: Path) -> list[Path]:
    if path.is_file():
        raise ValueError("Expected a skill directory or a folder containing skills")

    if (path / "SKILL.md").exists():
        return [path]

    return sorted([item for item in path.iterdir() if item.is_dir() and (item / "SKILL.md").exists()])


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_skill.py <skill-dir-or-skills-dir>")
        return 1

    target = Path(sys.argv[1]).resolve()
    if not target.exists():
        print(f"Path not found: {target}")
        return 1

    try:
        skill_dirs = collect_skill_dirs(target)
    except ValueError as exc:
        print(exc)
        return 1

    if not skill_dirs:
        print(f"No skills found under: {target}")
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill_dir(skill_dir))

    if errors:
        print("Validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_dirs)} skill(s) successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
