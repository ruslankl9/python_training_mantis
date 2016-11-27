import pytest
import os.path
import json
from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        target_filename = file
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), target_filename) \
            if os.path.basename(target_filename) == target_filename else target_filename
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture
def app(request):
    global fixture, target
    browser = request.config.getoption("--browser")
    config = load_config(request.config.getoption("--target"))
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config['web']['baseUrl'])
    fixture.session.ensure_login(username=config['webadmin']['username'], password=config['webadmin']['password'])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")