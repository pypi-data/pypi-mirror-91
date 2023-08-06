# -*- coding: utf-8 -*-

import pytest
import tuxsuite


@pytest.fixture(autouse=True)
def reset_config():
    tuxsuite.__config__ = None


@pytest.fixture
def params():
    return {
        "git_repo": "https://github.com/torvalds/linux.git",
        "git_ref": "master",
        "target_arch": "arm64",
        "toolchain": "gcc-9",
        "kconfig": ["defconfig"],
    }


def test_new_build(config, params):
    build = tuxsuite.Build(**params)
    assert build.token is not None
    assert build.kbapi_url is not None


def test_validate_auth_token_only_once(config, params, mocker):
    check_auth_token = mocker.patch("tuxsuite.config.Config.check_auth_token")
    tuxsuite.Build(**params)
    tuxsuite.Build(**params)
    assert check_auth_token.call_count == 1


def test_new_build_invalid_token(config, params, mocker):
    check_auth_token = mocker.patch("tuxsuite.config.Config.check_auth_token")
    check_auth_token.side_effect = RuntimeError("INVALID TOKEN")
    with pytest.raises(tuxsuite.exceptions.InvalidToken):
        tuxsuite.Build(**params)


def test_new_build_set(config, params):
    build_set = tuxsuite.BuildSet([params])
    assert build_set.kbapi_url is not None
