import re
import tempfile
import os

from utils import run_command_in_zsh


def is_private_ip(ip):
    """
    Check if the provided IP address is a private IPv4 address.

    Args:
    - ip (str): The IP address to check.

    Returns:
    - bool: True if the IP address is private, False otherwise.
    """
    # Regex pattern for private IPv4 addresses
    private_ipv4_pattern = re.compile(
        r"""
        \b
        (?:
            10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}              |   # 10.0.0.0 - 10.255.255.255
            172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.){1}[0-9]{1,3}   |   # 172.16.0.0 - 172.31.255.255
            192\.168\.(?:[0-9]{1,3}\.){1}[0-9]{1,3}          # 192.168.0.0 - 192.168.255.255
        )\b
    """,
        re.VERBOSE,
    )

    return bool(private_ipv4_pattern.match(ip))


def get_ip_tag(ips):
    # Create a temporary file to store the list of ips
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        for ip in ips:
            temp_file.write(f"{ip}\n")

    ips_file = temp_file.name
    command = f"cut-cdn -i {ips_file} --silent"

    results = run_command_in_zsh(command)
    os.remove(ips_file)

    if not len(results) == len(ips):
        return "cdn"

    for ip in ips:
        if not is_private_ip(ip):
            return "public"
    return "private"
