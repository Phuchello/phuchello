# TODO & Action Items — Phuchello Profile Repository

## Determinism Hotfix Tasks
- [x] Create `requirements.txt` with PyYAML dependency
- [x] Standardize `scripts/render_profile.py` on PyYAML (`yaml.safe_load`) exclusively
- [x] Update `.github/workflows/profile-check.yml` to install `requirements.txt`
- [x] Update `scripts/ci_test.py` and `scripts/test_profile.ps1` to include `requirements.txt`
- [x] Run local PowerShell test suite (`test_profile.ps1`)
- [ ] Push single unified commit to `origin/main`
- [ ] Verify remote GitHub Actions run completes with `conclusion: success`
