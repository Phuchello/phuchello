#!/usr/bin/env python3
"""
scripts/ci_test.py
==================
Self-contained CI validation suite for Phuchello profile repository.
Tests:
1. Required repository file hierarchy.
2. SVG asset validity (no malicious scripts, valid XML structure).
3. Deterministic rendering & drift check (render_profile.py --check).
4. Profile data reactivity (profile.yml controls rendered output).
5. Project registry reactivity (projects.yml controls rendered output).
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_file_hierarchy():
    print("[1/5] Verifying required file hierarchy...")
    required_files = [
        "README.md",
        "README.template.md",
        "PROJECT_STATE.md",
        "TODO.md",
        "ANTIGRAVITY_HANDOFF.md",
        "assets/network-banner.svg",
        "assets/topology.svg",
        "data/profile.yml",
        "data/projects.yml",
        "data/stack.yml",
        "scripts/render_profile.py",
    ]
    missing = [f for f in required_files if not (BASE_DIR / f).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing required repository files: {missing}")
    print("  [OK] All required files exist.")


def test_svg_assets():
    print("[2/5] Validating SVG vector integrity...")
    svgs = ["assets/network-banner.svg", "assets/topology.svg"]
    for svg_rel in svgs:
        svg_path = BASE_DIR / svg_rel
        content = svg_path.read_text(encoding="utf-8")
        if "<svg" not in content or "</svg>" not in content or "viewBox=" not in content:
            raise ValueError(f"Malformed SVG structure in: {svg_rel}")
        if "<script" in content or "javascript:" in content:
            raise SecurityError(f"Prohibited script tag detected in: {svg_rel}")
        print(f"  [OK] {svg_rel} is structurally valid and sanitized.")


def test_render_check():
    print("[3/5] Verifying rendered README sync (no drift)...")
    res = subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "render_profile.py"), "--check"],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr, file=sys.stderr)
        raise RuntimeError("render_profile.py --check failed. README.md is out of sync.")
    print("  [OK] README.md is strictly in sync with data models.")


def test_profile_reactivity():
    print("[4/5] Testing data/profile.yml reactivity...")
    profile_path = BASE_DIR / "data" / "profile.yml"
    bak_path = BASE_DIR / "data" / "profile.yml.ci_bak"
    test_readme = BASE_DIR / "README.test.md"

    shutil.copy(profile_path, bak_path)
    try:
        orig_text = profile_path.read_text(encoding="utf-8")
        test_marker = "TEST_NOC_LOCATION_CI_XYZ"
        modified_text = orig_text.replace("Ho Chi Minh City, Vietnam", test_marker)
        profile_path.write_text(modified_text, encoding="utf-8")

        res = subprocess.run(
            [sys.executable, str(BASE_DIR / "scripts" / "render_profile.py"), "--output", "README.test.md"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            raise RuntimeError(f"Renderer failed during profile reactivity test: {res.stderr}")

        output_text = test_readme.read_text(encoding="utf-8")
        if test_marker not in output_text:
            raise AssertionError("Renderer failed to reflect profile.yml location changes into output markdown.")
        print("  [OK] profile.yml data changes propagate directly to rendered README.")
    finally:
        if test_readme.exists():
            test_readme.unlink()
        if bak_path.exists():
            shutil.move(bak_path, profile_path)


def test_projects_reactivity():
    print("[5/5] Testing data/projects.yml reactivity...")
    projects_path = BASE_DIR / "data" / "projects.yml"
    bak_path = BASE_DIR / "data" / "projects.yml.ci_bak"
    test_readme = BASE_DIR / "README.test.md"

    dummy_entry = """
  - name: "AIoT Edge Telemetry Gateway"
    repo: "Phuchello/aiot-gateway-test"
    category: "Edge & Telemetry"
    tagline: "Test entry for automated CI data injection check"
    description: "Temporary validation entry verifying dynamic data rendering in CI."
    tech:
      - ESP32
      - MQTT
      - Python
    featured: true
    status: "Active"
    priority: 99
    links:
      repository: "https://github.com/Phuchello/aiot-gateway-test"
"""

    shutil.copy(projects_path, bak_path)
    try:
        with open(projects_path, "a", encoding="utf-8") as f:
            f.write(dummy_entry)

        res = subprocess.run(
            [sys.executable, str(BASE_DIR / "scripts" / "render_profile.py"), "--output", "README.test.md"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            raise RuntimeError(f"Renderer failed during projects reactivity test: {res.stderr}")

        output_text = test_readme.read_text(encoding="utf-8")
        if "AIoT Edge Telemetry Gateway" not in output_text:
            raise AssertionError("Renderer failed to reflect projects.yml injection into output markdown.")
        print("  [OK] projects.yml additions propagate directly to rendered README.")
    finally:
        if test_readme.exists():
            test_readme.unlink()
        if bak_path.exists():
            shutil.move(bak_path, projects_path)


def main():
    print("========================================")
    print("  PHUCHELLO PROFILE REPO CI VALIDATION  ")
    print("========================================")
    try:
        test_file_hierarchy()
        test_svg_assets()
        test_render_check()
        test_profile_reactivity()
        test_projects_reactivity()
        print("\n========================================")
        print("    ALL CI VALIDATION CHECKS PASSED     ")
        print("========================================")
        sys.exit(0)
    except Exception as e:
        print(f"\n[CI FAILURE] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
