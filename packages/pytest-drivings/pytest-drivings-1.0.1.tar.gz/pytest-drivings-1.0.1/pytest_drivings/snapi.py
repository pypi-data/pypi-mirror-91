import requests


class SNAPI:
    """
    Interface to the Selenium Node API.
    """

    @staticmethod
    def start(ip_address: str):
        """
        Starts a Selenium Server instance at an available port, returning the port number.
        :return:
        """
        return (
            requests.post(f"http://{ip_address}:8000/port", timeout=60)
            .json()
            .get("port", "")
        )

    @staticmethod
    def status(ip_address: str, port: str):
        """
        Checks whether or not the Selenium Server instance at the given port has started.
        :return:
        """
        return (
            requests.get(f"http://{ip_address}:8000/port/{port}", timeout=60)
            .json()
            .get("status", "")
            == "up"
        )

    @staticmethod
    def public_ip(ip_address: str):
        """
        Returns the public-facing IP address of the server.
        :return:
        """
        return (
            requests.get(f"http://{ip_address}:8000/public-ip", timeout=60)
            .json()
            .get("ip_address", "")
        )

    @staticmethod
    def kill_watchdog(ip_address: str):
        """
        Stops the watchdog service from running on the server.
        :return:
        """
        return (
            requests.post(
                f"http://{ip_address}:8000/kill-watchdog", timeout=60
            ).status_code
            == 200
        )

    @staticmethod
    def stop(ip_address: str, port: str, session_dir: str = None):
        """
        Stops the Selenium Server instance running at the specified port.
        Wipes the directory specified on the server, if any.
        :return:
        """
        return (
            requests.delete(
                f"http://{ip_address}:8000/port/{port}",
                data={"session_directory": session_dir} if session_dir else {},
                timeout=60,
            ).status_code
            == 200
        )

    @staticmethod
    def clear_session(ip_address: str, session_dir: str):
        return (
            requests.delete(
                f"http://{ip_address}:8000/session",
                data={"session_directory": session_dir},
                timeout=60,
            ).status_code
            == 200
        )
