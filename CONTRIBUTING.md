# Contributing to hermes-ecc

Thanks for contributing.

## Prerequisites

- Python 3.10+
- Git

## Local setup

```bash
git clone https://github.com/TheophilusChinomona/hermes-ecc.git
cd hermes-ecc
python -m pip install -U pytest
```

## Run tests

```bash
python -m pytest -q
```

Current tests cover:
- ECC auto-router behavior
- plugin pack integrity (plugin count, manifests, init modules, skills docs)
- interactive installer selection and copy behavior

## Plugin contribution rules

When adding or updating an `ecc-*` plugin:

1. Include `plugin.yaml`.
2. Include `__init__.py`.
3. For skill-pack plugins, include `skills/*.md`.
4. Keep `__pycache__/` and `*.pyc` out of version control.

## Pull requests

1. Create a feature branch.
2. Make focused changes.
3. Run tests and ensure they pass.
4. Open a PR with a short summary and test results.

## CI

GitHub Actions runs `pytest` on push and pull request via:
- `.github/workflows/tests.yml`
