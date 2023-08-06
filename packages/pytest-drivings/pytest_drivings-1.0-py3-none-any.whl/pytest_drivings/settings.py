"""
Plugin configuration. Allows number of vCPUs & GBs of RAM allocated
to each Selenium Server to be specified, as well as the number of
browsers to run on each server and the maximum number of servers
which may be created simultaneously.
"""
from collections import namedtuple
import os

Environment = namedtuple(
    "Environment", ["agent_params", "max_vms", "max_drivers_per_vm"]
)

# New environment, designed to run multiple browsers per VM with session isolation.
# Tested rigorously to achieve an ideal load average (~4.5)
MAX_DRIVER_ENV = Environment(
    agent_params={
        "os": "seleniumserver",
        "cpu_count": 2,
        "ram_amount": 5120,
        "os_volume": {"size": 10},
        "agent_type": "",
        "name": "selenium",
        "ttl": 8,
        "region": "nwk",
    },
    max_vms=45,
    max_drivers_per_vm=4,
)


# Stable environment designed to run multiple browsers per VM with session isolation.
# High RAM to hopefully prevent crashes.
# Drivers per VM tuned for stability
STABLE_ENV = Environment(
    agent_params={
        "os": "seleniumserver",
        "cpu_count": 2,
        "ram_amount": 16384,
        "os_volume": {"size": 10},
        "agent_type": "",
        "name": "selenium",
        "ttl": 8,
        "region": "nwk",
    },
    max_vms=80,
    max_drivers_per_vm=6,
)

SAFE_ENV = Environment(
    agent_params={
        "os": "seleniumserver",
        "cpu_count": 2,
        "ram_amount": 16384,
        "os_volume": {"size": 10},
        "agent_type": "",
        "name": "selenium",
        "ttl": 8,
        "region": "nwk",
    },
    max_vms=80,
    max_drivers_per_vm=os.environ.get("browsers_per_server", 2),
)

ACTIVE_ENV = SAFE_ENV


def max_runners():
    """
    Returns the maximum number of Remote WebDriver instances supported by the active configuration.
    """
    return ACTIVE_ENV.max_drivers_per_vm * ACTIVE_ENV.max_vms
