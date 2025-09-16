from utils import run_command_in_zsh
import tempfile, os, json


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def httpx(subdomains, domain):

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        for sub in subdomains:
            temp_file.write(f"{sub}\n")

    subdomains_file = temp_file.name

    command = f"httpx -l {subdomains_file} -silent -json -favicon -fhr -tech-detect -irh -include-chain -timeout 3 -retries 1 -threads 5 -rate-limit 4 -ports 443 -extract-fqdn -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0' -H 'Referer: https://{domain}'"

    print(f"{Colors.GRAY}Executing commands: {command}{Colors.RESET}")

    result = run_command_in_zsh(command, read_line=False)
    responses = []
    for r in result.splitlines():
        response = json.loads(r)
        responses.append(response)
    os.remove(subdomains_file)
    return responses
