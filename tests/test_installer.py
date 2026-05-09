from pathlib import Path

from installer import discover_plugins, parse_selection, install_selected_plugins


def test_discover_plugins_sorted(tmp_path):
    (tmp_path / "plugins").mkdir()
    (tmp_path / "plugins" / "ecc-zeta").mkdir()
    (tmp_path / "plugins" / "ecc-alpha").mkdir()
    (tmp_path / "plugins" / "not-ecc").mkdir()

    found = discover_plugins(tmp_path)
    assert found == ["ecc-alpha", "ecc-zeta"]


def test_parse_selection_all():
    assert parse_selection("all", 4) == [0, 1, 2, 3]


def test_parse_selection_csv_numbers():
    assert parse_selection("1,3,2", 4) == [0, 1, 2]


def test_parse_selection_rejects_out_of_range():
    try:
        parse_selection("5", 4)
    except ValueError as exc:
        assert "out of range" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_install_selected_plugins_copies_directories(tmp_path):
    repo_root = tmp_path / "repo"
    source = repo_root / "plugins"
    target = tmp_path / "target"
    (source / "ecc-alpha").mkdir(parents=True)
    (source / "ecc-alpha" / "plugin.yaml").write_text("name: alpha\n", encoding="utf-8")
    (source / "ecc-beta").mkdir(parents=True)
    (source / "ecc-beta" / "plugin.yaml").write_text("name: beta\n", encoding="utf-8")

    installed = install_selected_plugins(repo_root, target, ["ecc-beta"])

    assert installed == ["ecc-beta"]
    assert (target / "ecc-beta" / "plugin.yaml").is_file()
    assert not (target / "ecc-alpha").exists()
