import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pytest_drivings.local_webdriver import LocalWebDriver
from pytest_drivings.base_webdriver import BaseWebDriver as RemoteWebDriver
from qapi_client.v1.client import QApi
from qapi_client.v1.models.agent import CreateAgentPayload
from datetime import datetime
import logging
from atexit import register
import random
import string
import math
import pytest_drivings.settings as settings
import os
import shutil
import json
import time
import traceback
import sys
from pytest_drivings.snapi import SNAPI
import concurrent.futures as futures

# Debug mode flag - Can be set via GitLab environment variables or local environment variables
DEBUG_MODE = os.environ.get("DEBUG_MODE", 0) == 1

download_path_pref = {"download.default_directory": "/tmp/test-results/downloads"}

# Options/capabilities for a remote, headless Chromedriver instance
remote_options = webdriver.ChromeOptions()
remote_options.add_argument("headless")
remote_options.add_argument("disable-gpu")
remote_options.add_argument("enable-automation")
remote_options.add_argument("disable-extensions")
remote_options.add_argument("window-size=1920,1080")
remote_options.add_argument("start-maximized")
remote_options.add_experimental_option("prefs", download_path_pref)
remote_capabilities = remote_options.to_capabilities()
remote_capabilities["browserName"] = "chrome"
remote_capabilities["platform"] = "Linux"

# Options for a local, headed Chromedriver instance
local_options = webdriver.ChromeOptions()
local_options.add_argument("no-sandbox")
local_options.add_argument("window-size=1920,1080")
local_options.add_argument("start-maximized")
local_options.add_experimental_option("prefs", download_path_pref)

# settings to allow the webdriver to capture chrome console AND network logs
google_logging_prefs = {"browser": "ALL", "performance": "INFO"}


def pytest_addoption(parser):
    """
    Add a command line option to switch between using local and remote WebDrivers
    :param parser:
    :return: None
    """
    parser.addoption(
        "--local",
        action="store_true",
        default=False,
        help="Use local WebDriver (good for debugging tests)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode " "(doesn't take up your screen!)",
    )


def selenium_server_port(server_ip):
    """
    Starts the Selenium Server executable on an available port of this worker's QAPI server instance.
    Returns the port number on which the service was started.
    :return:
    """
    logging.info(
        f"Sending a Snapi request to start a Selenium Server instance on server {server_ip}"
    )
    port_number = SNAPI.start(server_ip)
    logging.info(f"Triggered a Selenium Server instance on {server_ip}:{port_number}")
    started = False
    attempts = 0
    while not started and attempts < 3:
        started = SNAPI.status(server_ip, port_number)
        attempts += 1
        if not started:
            time.sleep(attempts ** 2)
    assert (
        started
    ), f"Selenium Server instance at {server_ip}:{port_number} failed to start."
    logging.info(
        f"Confirmed via Snapi that Selenium Server has started at {server_ip}:{port_number}"
    )
    return port_number


def set_selenium_server_public_ip(server_ip):
    """
    This function executes some python on the selenium server, storing its public-facing IP
    as an environment variable, usable in tests.
    :param server_ip:
    :return:
    """
    result = SNAPI.public_ip(server_ip)
    assert len(result) > 0, "Server external IP could not be resolved, is QAPI running?"
    os.environ["server_external_ip"] = result


def create_webdriver(session_dir="/tmp/chrome", headless=False):
    if headless:
        local_options.add_argument("headless")
    # Ensure each webdriver will have a unique session directory
    local_options.add_argument(f"user-data-dir={session_dir}")

    desired_caps = DesiredCapabilities.CHROME.copy()
    desired_caps["goog:loggingPrefs"] = google_logging_prefs

    local_options.add_argument(f"user-data-dir={session_dir}")
    driver = LocalWebDriver(
        "chromedriver", options=local_options, desired_capabilities=desired_caps
    )
    return driver


@pytest.fixture(scope="function", autouse=True)
def web_driver(request):
    """
    Creates and yields a Local or Remote WebDriver instance,
    then destroys the instance after the test function completes.
    :param request: Request instance.
    :return: None
    """
    # Create a new (random) directory for the new WebDriver's session data
    session_handle = "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(10)]
    )
    session_dir = f"/tmp/profile-{session_handle}"
    if request.config.getoption("--local"):
        # Create a local Chromedriver instance with a unique session directory
        driver = create_webdriver(
            session_dir=session_dir, headless=request.config.getoption("--headless")
        )
        # Create function to reset driver session
        driver.clear_session = lambda: wipe_directory(session_dir)
    else:
        # Create Remote WebDriver instance using Selenium Server instance
        remote_options.add_argument(f"user-data-dir={session_dir}")
        remote_caps = remote_options.to_capabilities()
        remote_caps["browserName"] = "chrome"
        remote_caps["platform"] = "Linux"
        remote_caps["goog:loggingPrefs"] = google_logging_prefs
        attempts = 0
        driver = None
        while attempts < 3 and not driver:
            try:
                server = get_server(request.config)
                server_port = get_server_port(request.config)
                set_selenium_server_public_ip(server)
                logging.info(
                    f"Attempting to start a RemoteWebDriver on server {server}:{server_port}"
                )
                driver = RemoteWebDriver(
                    f"http://{server}:{server_port}/wd/hub", remote_caps
                )
            except:
                traceback.print_exc(file=sys.stdout)
                attempts += 1
                time.sleep(10 * (attempts ** 2))
        if DEBUG_MODE and not driver:
            # Keep the server alive to investigate the error
            # Kill the watchdog, Old Yeller style
            logging.debug(
                f"Sending Snapi request to stop watchdog so faulty server {server} can be investigated"
            )
            SNAPI.stop(get_server(request.config), server_port)
            # Extend the TTL by 24 hours so we can investigate in the morning
            logging.debug(
                f"Sending Qapi request to extend server TTL so faulty server {server} ({get_server_id(request.config)}) can be investigated"
            )
            QApi().renew_agent(get_server_id(request.config), 1)
        assert driver, (
            f"Failed to connect to the Selenium Server with IP address {get_server(request.config)} "
            f"after 3 attempts. Is the server online?"
        )
        # Create function to reset driver session
        driver.clear_session = lambda: SNAPI.clear_session(
            get_server(request.config), session_handle
        )
    # Provide webdriver to test session
    yield driver
    # Post-session teardown
    # Release WebDriver instance
    driver.quit()


def wipe_directory(path):
    """
    Recursively deletes all contents of the folder at the given path.
    :param path:
    :return:
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def get_server(config):
    """
    Returns the IP address of the server assigned to this test runner process.
    :param config:
    :return:
    """
    if hasattr(config, "workerinput"):
        return os.environ.get("server")
    else:
        return json.loads(os.environ.get("servers")).get("data")[0].get("ip")


def get_server_id(config):
    """
    Returns the QAPI ID of the server assigned to this test runner process.

    :param config:
    :return:
    """
    if hasattr(config, "workerinput"):
        return os.environ.get("server_id")
    else:
        return json.loads(os.environ.get("servers")).get("data")[0].get("id")


def get_server_port(config):
    """
    Returns the port number of the Selenium Server instance running on
    the server assigned to this test runner process.
    """
    if hasattr(config, "workerinput"):
        return os.environ.get("port")
    else:
        return json.loads(os.environ.get("servers")).get("data")[0].get("port")


def teardown():
    """
    Tears down Selenium Server and WebDriver instances.
    :return: None
    """
    try:
        for server in json.loads(os.environ.get("servers")).get("data"):
            try:
                # Kill Selenium Server app instance running on our server
                logging.info(
                    f"Tearing down server ({server.get('ip')} ({server.get('id')})) via QAPI DELETE request"
                )
                QApi().delete_agent(server.get("id"))
            except:
                pass
    except:
        pass


def pytest_keyboard_interrupt(excinfo):
    """
    Ensure that WebDriver and Selenium Server instances are torn down after
    a test run is terminated via a keyboard interrupt.
    :param excinfo: Exception info.
    :return: None
    """
    teardown()


def pytest_sessionfinish(session, exitstatus):
    """
    Ensure that WebDriver and Selenium Server instances are torn down after
    a test run is terminated for any reason.
    :param session: Session data.
    :param exitstatus: Exit status.
    :return: None
    """
    if not (
        session.config.getoption("--local") or hasattr(session.config, "workerinput")
    ):
        teardown()


def pytest_xdist_setupnodes(config, specs):
    """
    Assigns Selenium Server instances to Xdist worker processes.
    :param config:
    :param specs:
    :return:
    """
    if not config.getoption("--local"):
        for i in range(len(specs)):
            server_index = i // settings.ACTIVE_ENV.max_drivers_per_vm
            specs[i].env["server"] = (
                json.loads(os.environ.get("servers"))
                .get("data")[server_index]
                .get("ip")
            )
            specs[i].env["server_id"] = (
                json.loads(os.environ.get("servers"))
                .get("data")[server_index]
                .get("id")
            )
            specs[i].env["port"] = str(
                json.loads(os.environ.get("servers"))
                .get("data")[server_index]
                .get("port")
            )
            # setting automation_foundation driver key for parallel usage
            specs[i].env["AF_DRIVER_KEY"] = specs[i].id


def pytest_configure(config):
    """
    Creates the minimum number of Selenium Server instances required to
    support the requested number of workers.
    :param config:
    :return:
    """
    if not (config.getoption("--local") or hasattr(config, "workerinput")):
        workers = config.getoption("numprocesses")
        if not workers:
            workers = 1
        assert workers <= settings.max_runners(), (
            f"The maximum number of runners currently allowed is "
            f"{settings.max_runners()}."
        )
        vms_to_create = math.ceil(workers / settings.ACTIVE_ENV.max_drivers_per_vm)

        def destroy_servers(s):
            for server in s:
                QApi().delete_agent(server["id"])

        def attempt_server_creation():
            servers = []
            attempts = 3
            while attempts > 0 and len(servers) < vms_to_create:
                servers += create_servers(vms_to_create - len(servers))
                attempts -= 1
            return servers

        # attempt server creation in Norwalk
        logging.info("Attempting to create Selenium Server VMs in Norwalk")
        start_time = datetime.now()
        servers = attempt_server_creation()
        if len(servers) != vms_to_create:
            destroy_servers(servers)
            logging.warning(
                f"Failed to successfully create {vms_to_create} Selenium Servers in Norwalk after three attempts."
            )
            logging.info(f"Attempting to create fallback servers in Rochester...")
            settings.ACTIVE_ENV.agent_params["region"] = "roc"
            start_time = datetime.now()
            servers = attempt_server_creation()
            if len(servers) != vms_to_create:
                destroy_servers(servers)
                pytest.exit(
                    f"Failed to successfully create {vms_to_create} Selenium Servers "
                    f"in both Rochester and Norwalk after three attempts (each). Is QAPI working?"
                )
        logging.info(
            f"QAPI created {vms_to_create} Selenium Server VMs in {datetime.now()-start_time}"
        )
        os.environ["servers"] = json.dumps({"data": servers})
        if DEBUG_MODE:
            logging.debug(
                f"Servers to be used in this test run: {', '.join([server['ip']+':'+server['port'] + ' ('+server['id']+')' for server in servers])}"
            )


def create_server():
    """
    Issues a request to QAPI to create a Selenium Server VM and waits for the agent to start.
    :return:
    """
    agent = QApi().create_agent(CreateAgentPayload(**settings.ACTIVE_ENV.agent_params))
    agent = QApi().wait_for_agent_to_start(agent.id)
    port = selenium_server_port(agent.ip_address)
    return {"ip": agent.ip_address, "id": agent.id, "port": port}


def create_servers(num_servers):
    """
    Creates the specified number of Selenium Servers.
    Performs server creation concurrently for speed, rate-limits requests for stability.
    (QAPI doesn't like lots of requests at once)
    :param num_servers: The number of servers to create.
    :return:
    """
    batch_size = 10  # VMs to create at once
    with futures.ThreadPoolExecutor(batch_size) as pool:
        servers = [pool.submit(create_server) for _ in range(num_servers)]
    return [s.result() for s in futures.as_completed(servers)]


# Ensure that teardown will always occur at exit
register(teardown)
