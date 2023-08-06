
import logging
import sys
from pathlib import Path

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.python import Metafunc


from trafficgenerator.tgn_utils import ApiType, get_test_config


def tgn_pytest_addoption(parser: Parser, tgn_config: str) -> None:
    """ Add options to allow the user to determine which APIs and servers to test.

    :param parser: pytest parser to config.
    :param tgn_config: Full path to test configuration module.
    """
    if Path(tgn_config).exists():
        test_config = get_test_config(tgn_config)
        tgn_api = test_config.api
        tgn_server = test_config.server
    else:
        tgn_api = None
        tgn_server = None
        tgn_config = None
    parser.addoption('--tgn-api', action='append', default=tgn_api, help='api options: rest or tcl, where applicabble')
    parser.addoption('--tgn-server', action='append', default=tgn_server, help='server name in the configuration file')
    parser.addoption('--tgn-config', action='store', default=tgn_config, help='path to configuration file')


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """ Generate tests for each API and server from pytest options. """
    metafunc.parametrize('api', metafunc.config.getoption('--tgn-api'), indirect=True)
    metafunc.parametrize('server', metafunc.config.getoption('--tgn-server'), indirect=True)


@pytest.fixture(scope='session')
def logger() -> logging.Logger:
    """ Yields configured logger. """
    logger = logging.getLogger('tgn')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    yield logger


@pytest.fixture(scope='session')
def api(request: SubRequest) -> ApiType:
    """ Yield API type - generate tests will generate API types based on the api option. """
    yield ApiType[request.param]


@pytest.fixture(scope='session')
def server(request: SubRequest) -> str:
    """ Yields server name in confing file - generate tests will generate servers based on the server option. """
    yield request.param


@pytest.fixture(scope='session')
def server_properties(request: SubRequest, server: str) -> dict:
    """ Yields server properties dict for the requested server. """
    yield get_test_config(request.config.getoption('--tgn-config')).server_properties[server]
