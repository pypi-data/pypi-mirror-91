import pytest

from james.config import IgniteConfig, IgniteUnknownSettingError


@pytest.fixture
def config():
    return IgniteConfig(test_mode=True)


def test_config_callback(config):
    # repository_url is derived from project_name
    value = 'some-new-name'
    config.set('PROJECT', 'project_name', value)
    git_url = config.get('PROJECT', 'repository_url')
    assert value in git_url


def test_config_cleanup(config):
    config.set('PROJECT', 'deprecated_var', 'some value')
    config.cleanup()
    with pytest.raises(IgniteUnknownSettingError):
        config.get('PROJECT', 'deprecated_var')
