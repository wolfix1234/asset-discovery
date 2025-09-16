from utils import run_command_in_zsh
from config import config
import tempfile, os


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def nuclei(urls):

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        for url in urls:
            temp_file.write(f"{url}\n")

    urls_file = temp_file.name
    WATCH_DIR = config().get("WATCH_DIR")
    command = f"nuclei -l {urls_file} -config {WATCH_DIR}nuclei/public-config.yaml"

    print(f"{Colors.GRAY}Executing commands: {command}{Colors.RESET}")

    results = run_command_in_zsh(command, read_line=False)
    os.remove(urls_file)
    return results
