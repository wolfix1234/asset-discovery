from utils import run_command_in_zsh


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def abuseipdb(domain):
    command = (
        f'curl -s "https://www.abuseipdb.com/whois/{domain}" '
        '-H "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" '
        '-b "abuseipdb_session=YOUR-SESSION" | '
        "grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox} "
        "--color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox} "
        "--color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox} "
        f'-E "<li>\\w.*</li>" | sed -E "s/<\\/?li>//g" | sed "s|$|.{domain}|"'
    )

    print(f"{Colors.GRAY}Executing commands: {command}{Colors.RESET}")
    res = run_command_in_zsh(command)

    res_num = len(res) if res else 0
    print(f"{Colors.GRAY}done for {domain}, results: {res_num}{Colors.RESET}")

    return res
