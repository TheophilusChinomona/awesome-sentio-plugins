# awesome-sentio-plugins

[![Tests](https://github.com/TheophilusChinomona/awesome-sentio-plugins/actions/workflows/tests.yml/badge.svg)](https://github.com/TheophilusChinomona/awesome-sentio-plugins/actions/workflows/tests.yml)

Standalone repository for ECC plugins for Hermes/Athena.

## Contents

This repo contains the following plugin packs under `plugins/`:

- ecc-architecture
- ecc-auto-router
- ecc-code-review
- ecc-core
- ecc-cpp
- ecc-dart-flutter
- ecc-devops
- ecc-documentation
- ecc-dotnet
- ecc-extras
- ecc-go
- ecc-java-kotlin
- ecc-ml-ai
- ecc-perl
- ecc-php
- ecc-python
- ecc-rust
- ecc-security
- ecc-swift
- ecc-testing
- ecc-typescript

## Structure

```text
plugins/
  ecc-*/
    plugin.yaml
    __init__.py
    skills/*.md
```

## Usage

### Interactive installer (recommended)

Run the installer and choose exactly which plugins to install:

```bash
python installer.py
```

It will:
- show all available `ecc-*` plugins
- ask you to choose by number or `all`
- ask for install path (defaults to `~/.hermes/plugins`)

### Non-interactive installer (CI/automation)

Install specific plugins:

```bash
python installer.py --plugins ecc-core,ecc-python --target ~/.hermes/plugins
```

Install all plugins:

```bash
python installer.py --plugins all --target ~/.hermes/plugins
```

### Manual copy

Copy any `ecc-*` folder into your Hermes/Athena plugins directory:

```bash
cp -r plugins/ecc-python ~/.hermes/plugins/
```

Or copy all:

```bash
cp -r plugins/ecc-* ~/.hermes/plugins/
```

Then restart Hermes/Athena and list skills/plugins to verify they are available.

## Testing

Run tests locally:

```bash
python -m pip install -U pytest
python -m pytest -q
```

## Notes

- This repo mirrors plugin content from a working local Hermes plugin environment.
- `__pycache__` and `.pyc` artifacts are excluded.
