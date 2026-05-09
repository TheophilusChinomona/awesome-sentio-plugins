from __future__ import annotations

import shutil
from pathlib import Path


def discover_plugins(repo_root: Path) -> list[str]:
    plugins_dir = repo_root / "plugins"
    return sorted(p.name for p in plugins_dir.glob("ecc-*") if p.is_dir())


def parse_selection(raw: str, total: int) -> list[int]:
    text = raw.strip().lower()
    if text == "all":
        return list(range(total))

    chosen: set[int] = set()
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        if not token.isdigit():
            raise ValueError(f"invalid selection: {token}")
        idx = int(token)
        if idx < 1 or idx > total:
            raise ValueError(f"selection out of range: {idx}")
        chosen.add(idx - 1)

    if not chosen:
        raise ValueError("no valid selections")
    return sorted(chosen)


def install_selected_plugins(repo_root: Path, target_dir: Path, selected: list[str]) -> list[str]:
    source_root = repo_root / "plugins"
    target_dir.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    for name in selected:
        src = source_root / name
        dst = target_dir / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        installed.append(name)
    return installed


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    plugins = discover_plugins(repo_root)
    if not plugins:
        print("No ecc-* plugins found in ./plugins")
        return 1

    default_target = Path.home() / ".hermes" / "plugins"

    print("ECC Plugin Installer")
    print("====================")
    print("Available plugins:")
    for idx, name in enumerate(plugins, start=1):
        print(f"  {idx}. {name}")

    print()
    print("Enter plugin numbers separated by commas (e.g. 1,3,5) or 'all'.")
    selection_raw = input("Selection: ")

    try:
        indexes = parse_selection(selection_raw, len(plugins))
    except ValueError as exc:
        print(f"Invalid selection: {exc}")
        return 1

    selected_names = [plugins[i] for i in indexes]

    target_raw = input(f"Install path [{default_target}]: ").strip()
    target_dir = Path(target_raw).expanduser() if target_raw else default_target

    installed = install_selected_plugins(repo_root, target_dir, selected_names)

    print()
    print(f"Installed {len(installed)} plugin(s) to {target_dir}:")
    for name in installed:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
