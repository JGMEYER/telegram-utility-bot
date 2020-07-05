import os

import pytest
from unittest import TestCase

from ... import env


def _delenv_if_exists(monkeypatch, varname):
    if varname in os.environ:
        monkeypatch.delenv(varname)


# Keep these tests out of a TestCase to utilize pytest monkeypatch feature.
# Allows us to modify env variables in tests without impacting actual env.


def test_getenv_no_var_no_dev(monkeypatch):
    _delenv_if_exists(monkeypatch, "TEST_VAR")
    _delenv_if_exists(monkeypatch, "TEST_VAR_DEV")
    with pytest.raises(KeyError):
        env.getenv("TEST_VAR")


def test_getenv_has_var_no_dev(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "foo")
    _delenv_if_exists(monkeypatch, "TEST_VAR_DEV")
    var = env.getenv("TEST_VAR")
    assert var == "foo"


def test_getenv_no_var_has_dev(monkeypatch):
    _delenv_if_exists(monkeypatch, "TEST_VAR")
    monkeypatch.setenv("TEST_VAR_DEV", "bar")
    var = env.getenv("TEST_VAR")
    assert var, "bar"


def test_getenv_has_var_has_dev(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "foo")
    monkeypatch.setenv("TEST_VAR_DEV", "bar")
    var = env.getenv("TEST_VAR")
    assert var == "foo"
