"""The database drivers are optional extras, not dependencies of the library."""

import pathlib
import tomllib

PYPROJECT = pathlib.Path(__file__).parent.parent / "pyproject.toml"


def _project() -> dict:
    with open(PYPROJECT, "rb") as f:
        return tomllib.load(f)["project"]


def test_drivers_are_not_required():
    """Neither database driver is a required dependency."""
    required = " ".join(_project()["dependencies"])
    assert "mysqlclient" not in required
    assert "psycopg2" not in required


def test_drivers_are_extras():
    """Each driver is available as an extra."""
    extras = _project()["optional-dependencies"]
    assert any(d.startswith("mysqlclient") for d in extras["mysql"])
    assert any(d.startswith("psycopg2") for d in extras["postgres"])
