# ANTIGRAVITY HANDOFF BRIEF

## 1. What Was Built
A complete, maintainable, data-driven GitHub Profile repository for **Võ Trọng Phúc** (`Phuchello`), anchored in the **Network Intelligence / NOC Terminal** visual concept.

Key revisions & accomplishments:
- **True Source of Truth**: All profile-level content (identity, mission, role, overview, focus areas, current trajectory, and connect telemetry) is driven directly by `data/profile.yml`.
- **Credibility & Capability Calibration**: Replaced hyperbolic copy with grounded technical language reflecting an undergraduate student focused on network systems, AIoT pipelines, and research-oriented architectures.
- **Three-Tier Capability Matrix**: Technical skills in `data/stack.yml` explicitly indicate maturity (`Demonstrated`, `Practicing`, `Exploring`) across 5 system layers.
- **Navigation-Oriented Project Cards**: Project descriptions in `data/projects.yml` are concise and direct visitors to repositories and documentation without marketing fluff.
- **Custom NOC Visuals**: Vector assets (`assets/network-banner.svg` and `assets/topology.svg`) using a restrained dark palette (`#070B14`, `#00E5FF`, `#38BDF8`, `#22C55E`).
- **Zero-Dependency Python Generator & CI Runner**: `scripts/render_profile.py` and `scripts/ci_test.py` execute cleanly in CI and locally without third-party dependencies.

---

## 2. File Architecture
```text
Phuchello/
├── README.md                          # Deterministically rendered GitHub Profile README
├── README.template.md                 # Structural template with 6 data-driven block tokens
├── PROJECT_STATE.md                   # Real-time milestone tracker & architectural decisions
├── TODO.md                            # Completed checklist & inspection logs
├── ANTIGRAVITY_HANDOFF.md             # This handoff brief
├── assets/
│   ├── network-banner.svg             # NOC terminal banner (EDGE ─── NETWORK ─── CLOUD ─── INTEL)
│   └── topology.svg                   # Edge-to-Cloud system architecture & research trajectory
├── data/
│   ├── profile.yml                    # Source of truth for identity, overview, trajectory, links
│   ├── projects.yml                   # Priority-ordered featured & future project registry
│   └── stack.yml                      # System-layered technical capabilities with maturity tiers
├── scripts/
│   ├── render_profile.py              # Zero-dependency Python renderer & validator
│   ├── ci_test.py                     # Self-contained CI validation suite
│   └── test_profile.ps1               # Local PowerShell validation suite
└── .github/
    └── workflows/
        └── profile-check.yml          # GitHub Actions CI workflow (drift & reactivity check)
```

---

## 3. Commands to Validate

### A. Regenerate README from Data
```bash
python scripts/render_profile.py
```

### B. Validate CI Drift & Schema Integrity
```bash
python scripts/render_profile.py --check
```

### C. Run Local PowerShell Test Suite (Windows)
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test_profile.ps1
```

---

## 4. Known Trade-Offs & Limitations
1. **Zero-Dependency Native YAML Parser**: `scripts/render_profile.py` implements a robust parser for the specific YAML structures in `data/*.yml` with transparent fallback to PyYAML if installed. It supports standard scalars, lists, mappings, and block strings.
2. **Restrained Social Badges**: Uses two minimal shields.io badges for GitHub and LinkedIn rather than generic metric/trophy counters.
3. **Conceptual Topology vs Deployed Architecture**: `assets/topology.svg` is explicitly labeled as a conceptual map of engineering exploration to maintain technical honesty.

---

## 5. Exact Files Downstream Reviewers / Codex Should Inspect
1. `README.md`
2. `README.template.md`
3. `data/profile.yml`
4. `data/projects.yml`
5. `data/stack.yml`
6. `assets/network-banner.svg`
7. `assets/topology.svg`
8. `scripts/render_profile.py`
9. `scripts/ci_test.py`
10. `.github/workflows/profile-check.yml`

---

## 6. Explicit Instruction to Codex / Downstream Reviewer

> **Do not redesign the profile from scratch. Perform a surgical final audit and fix only verified weaknesses.**
