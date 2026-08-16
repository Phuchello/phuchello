# ANTIGRAVITY HANDOFF BRIEF

## 1. What Was Built
A complete, maintainable, data-driven GitHub Profile repository for **Võ Trọng Phúc** (`Phuchello`), anchored in the **Network Intelligence / NOC Terminal** visual concept.

Key revisions & accomplishments:
- **True Source of Truth**: All profile-level content (identity, mission, role, overview, focus areas, current trajectory, and connect telemetry) is driven directly by `data/profile.yml`.
- **Single Canonical YAML Parser**: `scripts/render_profile.py` uses PyYAML exclusively (`requirements.txt`), guaranteeing 100% determinism across local development and GitHub Actions CI.
- **Credibility & Capability Calibration**: Replaced hyperbolic copy with grounded technical language reflecting an undergraduate student focused on network systems, AIoT pipelines, and research-oriented architectures.
- **Three-Tier Capability Matrix**: Technical skills in `data/stack.yml` explicitly indicate maturity (`Demonstrated`, `Practicing`, `Exploring`) across 5 system layers.
- **Navigation-Oriented Project Cards**: Project descriptions in `data/projects.yml` are concise and direct visitors to repositories and documentation without marketing fluff.
- **Custom NOC Visuals**: Vector assets (`assets/network-banner.svg` and `assets/topology.svg`) using a restrained dark palette (`#070B14`, `#00E5FF`, `#38BDF8`, `#22C55E`).

---

## 2. File Architecture
```text
Phuchello/
├── README.md                          # Deterministically rendered GitHub Profile README
├── README.template.md                 # Structural template with 6 data-driven block tokens
├── PROJECT_STATE.md                   # Real-time milestone tracker & architectural decisions
├── TODO.md                            # Completed checklist & inspection logs
├── ANTIGRAVITY_HANDOFF.md             # This handoff brief
├── requirements.txt                   # Production dependency declaration (PyYAML)
├── assets/
│   ├── network-banner.svg             # NOC terminal banner (EDGE ─── NETWORK ─── CLOUD ─── INTEL)
│   └── topology.svg                   # Edge-to-Cloud system architecture & research trajectory
├── data/
│   ├── profile.yml                    # Source of truth for identity, overview, trajectory, links
│   ├── projects.yml                   # Priority-ordered featured & future project registry
│   └── stack.yml                      # System-layered technical capabilities with maturity tiers
├── scripts/
│   ├── render_profile.py              # Canonical PyYAML renderer & validator
│   ├── ci_test.py                     # Self-contained CI validation suite
│   └── test_profile.ps1               # Local PowerShell validation suite
└── .github/
    └── workflows/
        └── profile-check.yml          # GitHub Actions CI workflow (installs requirements.txt & runs ci_test.py)
```

---

## 3. Commands to Validate

### A. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### B. Regenerate README from Data
```bash
python scripts/render_profile.py
```

### C. Validate CI Drift & Schema Integrity
```bash
python scripts/render_profile.py --check
```

### D. Run CI Validation Suite
```bash
python scripts/ci_test.py
```

### E. Run Local PowerShell Test Suite (Windows)
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test_profile.ps1
```

---

## 4. Known Trade-Offs & Limitations
1. **PyYAML Dependency**: Single canonical parser declared in `requirements.txt` to eliminate dual-parser divergence.
2. **Restrained Social Badges**: Uses two minimal shields.io badges for GitHub and LinkedIn rather than generic metric/trophy counters.
3. **Conceptual Topology vs Deployed Architecture**: `assets/topology.svg` is explicitly labeled as a conceptual map of engineering exploration to maintain technical honesty.

---

## 5. Exact Files Downstream Reviewers / Codex Should Inspect
1. `README.md`
2. `README.template.md`
3. `requirements.txt`
4. `data/profile.yml`
5. `data/projects.yml`
6. `data/stack.yml`
7. `assets/network-banner.svg`
8. `assets/topology.svg`
9. `scripts/render_profile.py`
10. `scripts/ci_test.py`
11. `.github/workflows/profile-check.yml`

---

## 6. Explicit Instruction to Codex / Downstream Reviewer

> **Do not redesign the profile from scratch. Perform a surgical final audit and fix only verified weaknesses.**
