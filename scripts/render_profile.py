#!/usr/bin/env python3
"""
scripts/render_profile.py
=========================
Deterministic, data-driven README generator for Võ Trọng Phúc (@Phuchello).
Renders README.md from data/*.yml and README.template.md using PyYAML (yaml.safe_load).

Single canonical YAML interpretation ensures 100% determinism between local and CI environments.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import yaml
except ImportError:
    sys.exit(
        "[ERROR] PyYAML is required but not installed.\n"
        "Please install project dependencies by running:\n"
        "    pip install -r requirements.txt\n"
    )


def load_yaml_file(filepath: Path) -> Any:
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return yaml.safe_load(content)


def validate_profile(profile: Dict[str, Any]) -> None:
    if not isinstance(profile, dict):
        raise ValueError("profile.yml root must be a dictionary.")
    
    identity = profile.get("identity", {})
    for req in ["name", "handle", "role", "institution", "location", "tagline"]:
        if req not in identity or not str(identity[req]).strip():
            raise ValueError(f"profile.yml identity missing required field: '{req}'")

    if "overview" not in profile or "summary" not in profile["overview"]:
        raise ValueError("profile.yml missing overview.summary")


def validate_projects(projects: List[Dict[str, Any]]) -> None:
    required_fields = ["name", "repo", "category", "tagline", "tech", "featured", "status"]
    seen_repos = set()
    for idx, p in enumerate(projects):
        if not isinstance(p, dict):
            raise ValueError(f"Project item #{idx+1} is not a valid dictionary.")
        for f in required_fields:
            if f not in p:
                raise ValueError(f"Project #{idx+1} ({p.get('name', 'Unknown')}) missing required field: '{f}'")
        repo = p["repo"]
        if repo in seen_repos:
            raise ValueError(f"Duplicate project repository detected: {repo}")
        seen_repos.add(repo)
        if not isinstance(p["tech"], list) or len(p["tech"]) == 0:
            raise ValueError(f"Project '{p['name']}' must contain a non-empty list for 'tech'.")


def format_overview(profile_data: Dict[str, Any]) -> str:
    overview = profile_data.get("overview", {})
    focus_areas = overview.get("focus_areas", [])

    lines = []
    for fa in focus_areas:
        title = fa.get("title", "")
        desc = fa.get("desc", "")
        lines.append(f"* **{title}** — {desc}")

    return "\n".join(lines).strip()


def format_intro(profile_data: Dict[str, Any]) -> str:
    identity = profile_data.get("identity", {})
    intro = profile_data.get("intro", {})
    name = identity.get("name", "")
    descriptor = intro.get("descriptor", "")
    supporting = intro.get("supporting", "")
    lines = []
    if name and descriptor:
        lines.append(f"**{name}** — {descriptor}")
    elif name:
        lines.append(f"**{name}**")
    elif descriptor:
        lines.append(descriptor)
    if supporting:
        if lines:
            lines.append("")
        lines.append(supporting)
    return "\n".join(lines).strip()


def format_interest_block(profile_data: Dict[str, Any], key: str) -> str:
    interests = profile_data.get(key, [])
    if not interests:
        return "*No exploration areas configured.*"

    lines = []
    for item in interests:
        title = item.get("title", "")
        desc = item.get("desc", "")
        lines.append(f"* **{title}** — {desc}")

    return "\n".join(lines).strip()


def format_connect_block(profile_data: Dict[str, Any]) -> str:
    terminal_status = profile_data.get("terminal_status", {})
    social_links = profile_data.get("social", [])

    prompt = terminal_status.get("prompt", "[phuchello@workspace ~]$")
    entries = terminal_status.get("entries", [])
    terminal_lines = []
    for entry in entries:
        command = entry.get("command", "status")
        response = entry.get("response", "Networks → Edge Systems → Intelligence")
        terminal_lines.extend([f"{prompt} {command}", response])
    if not terminal_lines:
        terminal_lines = [f"{prompt} direction", "Networks → Edge Systems → Intelligence"]
    terminal_output = "\n".join(terminal_lines)

    badges = []
    for s in social_links:
        label = s.get("label", "Link")
        username = s.get("username", "")
        url = s.get("url", "")
        color = s.get("color", "315F57")
        logo = s.get("logo", "github")
        logo_color = s.get("logo_color", "F2F1ED")
        badge = f"[![{label}](https://img.shields.io/badge/{label}-{username}-{color}?style=flat-square&logo={logo}&logoColor={logo_color})]({url})"
        badges.append(badge)

    badge_line = " ".join(badges)

    return f"""<div align="center">

```text
{terminal_output}
```

{badge_line}

</div>""".strip()


def format_stack_markdown(stack_data: Dict[str, Any]) -> str:
    summary = stack_data.get("public_summary", [])
    if not summary:
        return "*No stack layers configured.*"

    output = ["| Area | Working with |", "|---|---|"]
    for item in summary:
        output.append(f"| **{item.get('area', 'Area')}** | {item.get('tools', '')} |")
    return "\n".join(output)


def format_projects_markdown(projects_data: Dict[str, Any]) -> str:
    projects = projects_data.get("projects", [])
    validate_projects(projects)

    # Filter featured and sort by priority (lowest integer = highest priority)
    featured = [p for p in projects if p.get("featured", False)]
    featured.sort(key=lambda x: x.get("priority", 999))

    if not featured:
        return "*No featured projects active.*"

    cards = []
    for p in featured:
        name = p["name"]
        repo = p["repo"]
        category = p.get("category", "Engineering")
        tagline = p.get("tagline", "")
        description = p.get("description", "").strip()
        status = p.get("status", "Active")
        tech_list = p.get("tech", [])
        links = p.get("links", {})

        repo_url = f"https://github.com/{repo}"
        tech_badges = " · ".join([f"`{t}`" for t in tech_list])

        link_items = []
        for label, url in links.items():
            clean_label = label.replace("_", " ").title()
            link_items.append(f"[{clean_label}]({url})")
        link_str = " · ".join(link_items) if link_items else f"[Repository]({repo_url})"

        card = f"""### [{name}]({repo_url})
**Category:** `{category}` &nbsp;|&nbsp; **Status:** `{status}` &nbsp;|&nbsp; **Stack:** {tech_badges}

> **{tagline}**

{description}

🔗 **Links:** {link_str}
"""
        cards.append(card.strip())

    return "\n\n---\n\n".join(cards)


def render_profile(
    template_path: Path,
    data_dir: Path,
    output_path: Optional[Path] = None,
    check_mode: bool = False,
) -> bool:
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    profile_file = data_dir / "profile.yml"
    projects_file = data_dir / "projects.yml"
    stack_file = data_dir / "stack.yml"

    profile_data = load_yaml_file(profile_file)
    projects_data = load_yaml_file(projects_file)
    stack_data = load_yaml_file(stack_file)

    validate_profile(profile_data)
    validate_projects(projects_data.get("projects", []))

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    rendered = template
    intro_block = format_intro(profile_data)
    overview_block = format_overview(profile_data)
    research_interests_block = format_interest_block(profile_data, "research_interests")
    stack_block = format_stack_markdown(stack_data)
    connect_block = format_connect_block(profile_data)

    rendered = rendered.replace("{{INTRO_BLOCK}}", intro_block)
    rendered = rendered.replace("{{OVERVIEW_BLOCK}}", overview_block)
    rendered = rendered.replace("{{RESEARCH_INTERESTS_BLOCK}}", research_interests_block)
    rendered = rendered.replace("{{SYSTEM_STACK_BLOCK}}", stack_block)
    rendered = rendered.replace("{{CONNECT_BLOCK}}", connect_block)

    # Clean trailing whitespaces and normalize line endings to Unix LF
    rendered = "\n".join([line.rstrip() for line in rendered.splitlines()]) + "\n"

    if check_mode:
        if not output_path or not output_path.exists():
            print(f"[CHECK FAILED] Output file does not exist: {output_path}", file=sys.stderr)
            return False
        with open(output_path, "r", encoding="utf-8") as f:
            existing = f.read()
        existing_normalized = "\n".join([line.rstrip() for line in existing.splitlines()]) + "\n"
        if existing_normalized != rendered:
            print(f"[CHECK FAILED] {output_path} is out of sync with data templates. Run 'python scripts/render_profile.py' to regenerate.", file=sys.stderr)
            return False
        print(f"[CHECK PASSED] {output_path} is strictly in sync with data models.")
        return True

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"[SUCCESS] Rendered {output_path} successfully from {data_dir}.")
    else:
        sys.stdout.write(rendered)

    return True


def main():
    parser = argparse.ArgumentParser(description="Render GitHub Profile README deterministically.")
    parser.add_argument("--template", type=str, default="README.template.md", help="Path to template file.")
    parser.add_argument("--data-dir", type=str, default="data", help="Directory containing YAML configuration.")
    parser.add_argument("--output", type=str, default="README.md", help="Target output markdown file.")
    parser.add_argument("--check", action="store_true", help="Check if output matches rendered template without modifying.")

    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    template_path = (base_dir / args.template) if not Path(args.template).is_absolute() else Path(args.template)
    data_dir = (base_dir / args.data_dir) if not Path(args.data_dir).is_absolute() else Path(args.data_dir)
    output_path = (base_dir / args.output) if not Path(args.output).is_absolute() else Path(args.output)

    try:
        success = render_profile(
            template_path=template_path,
            data_dir=data_dir,
            output_path=output_path,
            check_mode=args.check,
        )
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Renderer execution failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
