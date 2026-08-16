#!/usr/bin/env python3
"""
scripts/render_profile.py
=========================
Deterministic, data-driven README generator for Võ Trọng Phúc (@Phuchello).
Renders README.md from data/*.yml and README.template.md.

Zero external dependencies required (uses built-in parser with fallback to PyYAML if present).
"""

import sys
import os
import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# Try importing pyyaml, else fallback to built-in clean YAML parser
try:
    import yaml
    HAS_PYYAML = True
except ImportError:
    HAS_PYYAML = False


def _parse_scalar(val: str) -> Any:
    val = val.strip()
    if not val:
        return ""
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() in ("null", "none", "~"):
        return None
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        return val


def parse_simple_yaml(text: str) -> Any:
    """
    Robust, lightweight YAML parser for dictionaries, lists, and multi-line strings.
    Handles standard YAML used in configuration files without external dependencies.
    """
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Strip inline comments if not inside quotes
        if "#" in line:
            in_quote = False
            quote_char = ""
            comment_idx = -1
            for i, c in enumerate(line):
                if c in ('"', "'"):
                    if not in_quote:
                        in_quote = True
                        quote_char = c
                    elif quote_char == c:
                        in_quote = False
                elif c == "#" and not in_quote:
                    comment_idx = i
                    break
            if comment_idx != -1:
                line = line[:comment_idx].rstrip()
                if not line.strip():
                    continue
        indent = len(line) - len(line.lstrip(" "))
        cleaned_lines.append((indent, line.strip()))

    if not cleaned_lines:
        return {}

    def parse_block(idx: int, min_indent: int) -> (Any, int):
        if idx >= len(cleaned_lines):
            return {}, idx

        first_indent, first_line = cleaned_lines[idx]
        if first_line.startswith("- "):
            # Sequence
            res_list = []
            cur_idx = idx
            while cur_idx < len(cleaned_lines):
                indent, line = cleaned_lines[cur_idx]
                if indent < min_indent:
                    break
                if line.startswith("- "):
                    item_str = line[2:].strip()
                    if item_str.startswith(">") or item_str.startswith("|"):
                        # Multi-line block scalar in list item
                        block_lines = []
                        sub_idx = cur_idx + 1
                        while sub_idx < len(cleaned_lines):
                            s_indent, s_line = cleaned_lines[sub_idx]
                            if s_indent <= indent:
                                break
                            block_lines.append(s_line)
                            sub_idx += 1
                        sep = " " if item_str.startswith(">") else "\n"
                        res_list.append(sep.join(block_lines))
                        cur_idx = sub_idx
                    elif ":" in item_str and not (item_str.startswith('"') or item_str.startswith("'")):
                        # Inline dict starting on list item line
                        k, v = item_str.split(":", 1)
                        k = _parse_scalar(k)
                        v = v.strip()
                        sub_dict = {}
                        if v.startswith(">") or v.startswith("|"):
                            block_lines = []
                            sub_idx = cur_idx + 1
                            while sub_idx < len(cleaned_lines):
                                s_indent, s_line = cleaned_lines[sub_idx]
                                if s_indent <= indent:
                                    break
                                block_lines.append(s_line)
                                sub_idx += 1
                            sep = " " if v.startswith(">") else "\n"
                            sub_dict[k] = sep.join(block_lines)
                            cur_idx = sub_idx
                        elif v:
                            sub_dict[k] = _parse_scalar(v)
                            cur_idx += 1
                        else:
                            # Sub-block under this key
                            sub_val, next_i = parse_block(cur_idx + 1, indent + 2)
                            sub_dict[k] = sub_val
                            cur_idx = next_i

                        # Read subsequent keys for the same list item dict
                        while cur_idx < len(cleaned_lines):
                            s_indent, s_line = cleaned_lines[cur_idx]
                            if s_indent <= indent or s_line.startswith("- "):
                                break
                            if ":" in s_line:
                                sk, sv = s_line.split(":", 1)
                                sk = _parse_scalar(sk)
                                sv = sv.strip()
                                if sv.startswith(">") or sv.startswith("|"):
                                    block_lines = []
                                    sub_idx = cur_idx + 1
                                    while sub_idx < len(cleaned_lines):
                                        ss_indent, ss_line = cleaned_lines[sub_idx]
                                        if ss_indent <= s_indent:
                                            break
                                        block_lines.append(ss_line)
                                        sub_idx += 1
                                    sep = " " if sv.startswith(">") else "\n"
                                    sub_dict[sk] = sep.join(block_lines)
                                    cur_idx = sub_idx
                                elif sv:
                                    sub_dict[sk] = _parse_scalar(sv)
                                    cur_idx += 1
                                else:
                                    sub_val, next_i = parse_block(cur_idx + 1, s_indent + 1)
                                    sub_dict[sk] = sub_val
                                    cur_idx = next_i
                            else:
                                cur_idx += 1
                        res_list.append(sub_dict)
                    else:
                        res_list.append(_parse_scalar(item_str))
                        cur_idx += 1
                else:
                    break
            return res_list, cur_idx
        else:
            # Mapping
            res_dict = {}
            cur_idx = idx
            while cur_idx < len(cleaned_lines):
                indent, line = cleaned_lines[cur_idx]
                if indent < min_indent:
                    break
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = _parse_scalar(k)
                    v = v.strip()
                    if v.startswith(">") or v.startswith("|"):
                        block_lines = []
                        sub_idx = cur_idx + 1
                        while sub_idx < len(cleaned_lines):
                            s_indent, s_line = cleaned_lines[sub_idx]
                            if s_indent <= indent:
                                break
                            block_lines.append(s_line)
                            sub_idx += 1
                        sep = " " if v.startswith(">") else "\n"
                        res_dict[k] = sep.join(block_lines)
                        cur_idx = sub_idx
                    elif v:
                        res_dict[k] = _parse_scalar(v)
                        cur_idx += 1
                    else:
                        sub_val, next_i = parse_block(cur_idx + 1, indent + 1)
                        res_dict[k] = sub_val
                        cur_idx = next_i
                else:
                    cur_idx += 1
            return res_dict, cur_idx

    result, _ = parse_block(0, 0)
    return result


def load_yaml_file(filepath: Path) -> Any:
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if HAS_PYYAML:
        return yaml.safe_load(content)
    return parse_simple_yaml(content)


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


def format_stack_markdown(stack_data: Dict[str, Any]) -> str:
    layers = stack_data.get("layers", [])
    if not layers:
        return "*No stack layers configured.*"

    output = []
    for layer in layers:
        name = layer.get("name", "SYSTEM LAYER")
        desc = layer.get("description", "")
        items = layer.get("items", [])
        
        output.append(f"### `// LAYER :: {name}`")
        if desc:
            output.append(f"> *{desc}*")
            output.append("")

        output.append("| Capability | Focus / Engineering Details |")
        output.append("|---|---|")
        for it in items:
            it_name = it.get("name", "")
            it_detail = it.get("detail", "")
            output.append(f"| **{it_name}** | {it_detail} |")
        output.append("")
    return "\n".join(output).strip()


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

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    stack_block = format_stack_markdown(stack_data)
    projects_block = format_projects_markdown(projects_data)

    rendered = template.replace("{{SYSTEM_STACK_BLOCK}}", stack_block)
    rendered = rendered.replace("{{FEATURED_PROJECTS_BLOCK}}", projects_block)

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
