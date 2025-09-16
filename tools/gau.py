from utils import run_command_in_zsh


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def gau(domain):
    command = f"gau {domain} --threads 10 --subs | unfurl domain | sort -u"
    print(f"{Colors.GRAY}Executing commands: {command}{Colors.RESET}")
    res = run_command_in_zsh(command)
    res_num = len(res) if res else 0
    print(f"{Colors.GRAY}done for {domain}, results: {res_num}{Colors.RESET}")
    return res
