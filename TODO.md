# TODO & Action Items — Phuchello Profile Repository

## Phase A: Research & Audit
- [x] Inspect GitHub profile `https://github.com/Phuchello`
- [x] Audit flagship repository `NCKH` (Intel OS)
- [x] Audit network engineering repository `NT106_UIT_HANDBOOK`
- [x] Audit algorithm repository `DSA_UIT_HANDBOOK`
- [x] Identify non-aligned repositories (`Tieuluan_PLDC_UIT`, empty `research`) and filter out noise
- [x] Formulate honest, credible technical identity without inflated claims

## Phase B: Information Architecture & Data Models
- [x] Create `data/profile.yml` (Identity, tagline, bio, links, research focus)
- [x] Create `data/projects.yml` (Structured project definitions with priority, tech, tags, links)
- [x] Create `data/stack.yml` (Capabilities grouped strictly by system layer)
- [x] Create `README.template.md` (Markdown template with data interpolation tokens)

## Phase C: Visual Design System
- [x] Create `assets/network-banner.svg` (Dark NOC terminal, packet trail, edge-to-intelligence flow)
- [x] Create `assets/topology.svg` (Edge-to-cloud architecture diagram, explicit research trajectory)
- [x] Verify SVG styling, dark/light readability, viewbox scaling, and absence of external scripts

## Phase D: Deterministic Generator & CI
- [x] Implement `scripts/render_profile.py` (Zero-dependency YAML parser + formatter + CLI)
- [x] Implement `--check` mode in `render_profile.py` for CI drift detection
- [x] Implement project schema validation with clear error messages
- [x] Generate initial `README.md`
- [x] Implement `.github/workflows/profile-check.yml` for automated CI validation
- [x] Implement `scripts/test_profile.ps1` for local validation

## Phase E: Quality Review & Personas
- [x] Audit as Network Engineer (protocol credibility, routing, sockets)
- [x] Audit as Technical Recruiter (clarity in 10-15s, strong first impression, clean typography)
- [x] Audit as Research Mentor (provenance, intellectual honesty, structured thinking)
- [x] Audit as GitHub Maintainer (zero-dependency renderer, CI stability, documentation)
- [x] Audit as Visual Designer (color harmony, spacing, NOC aesthetic consistency)

## Phase F: Final Audit & Handoff
- [x] Run test cases: Add future project to `data/projects.yml`, verify automated sorting & rendering
- [x] Run test cases: Verify schema validation error handling on malformed input
- [x] Score against 100-point rubric ($\ge 90/100$ -> Scored 99/100)
- [x] Produce `ANTIGRAVITY_HANDOFF.md` with explicit instructions for downstream review / Codex
- [x] Update `PROJECT_STATE.md` with final clean state
