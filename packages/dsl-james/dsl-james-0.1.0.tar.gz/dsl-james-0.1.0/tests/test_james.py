#!/usr/bin/env python

"""Tests for `james` package."""

import pytest

from james.james import Ignition
from james.config import IgniteConfig, IgniteUnknownSettingError


@pytest.fixture
def ignition():
    return Ignition(
        config=IgniteConfig()
    )


def test_get(ignition):
    assert ignition.get('PROJECT', 'project_name') is not None
    with pytest.raises(IgniteUnknownSettingError):
        ignition.get('invalid section', 'bla')
    with pytest.raises(IgniteUnknownSettingError):
        ignition.get('PROJECT', 'invalid non-existing option')
