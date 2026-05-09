from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / "plugins"


def test_expected_ecc_plugin_count():
    plugin_dirs = sorted(p for p in PLUGINS_DIR.glob("ecc-*") if p.is_dir())
    assert len(plugin_dirs) == 21


def test_every_plugin_has_manifest_and_init():
    plugin_dirs = sorted(p for p in PLUGINS_DIR.glob("ecc-*") if p.is_dir())
    for plugin_dir in plugin_dirs:
        assert (plugin_dir / "plugin.yaml").is_file(), f"missing plugin.yaml in {plugin_dir.name}"
        assert (plugin_dir / "__init__.py").is_file(), f"missing __init__.py in {plugin_dir.name}"


def test_every_plugin_has_skills_markdown_except_router():
    plugin_dirs = sorted(p for p in PLUGINS_DIR.glob("ecc-*") if p.is_dir())
    for plugin_dir in plugin_dirs:
        if plugin_dir.name == "ecc-auto-router":
            continue
        skills_dir = plugin_dir / "skills"
        assert skills_dir.is_dir(), f"missing skills/ directory in {plugin_dir.name}"
        assert any(skills_dir.glob("*.md")), f"no markdown skills in {plugin_dir.name}"


def test_required_workflows_exist_for_ci_cd():
    workflows_dir = ROOT / ".github" / "workflows"
    required = ["tests.yml", "lint.yml", "security.yml", "release.yml"]
    for workflow in required:
        assert (workflows_dir / workflow).is_file(), f"missing workflow {workflow}"
