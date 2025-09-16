import os
import tempfile
from utils import run_command_in_zsh

from database.selectors import get_subdomains, get_lives


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def dynamic_brute(domain):
    # Paths for temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        dns_brute = os.path.join(temp_dir, f"{domain}.dns_brute")
        dns_gen_words = os.path.join(temp_dir, "dnsgen-words.tx")
        alt_dns_words = os.path.join(temp_dir, "altdns-words.txt")
        merged_path = os.path.join(temp_dir, "words-merged.tx")
        domain_dns_gen = os.path.join(temp_dir, f"{domain}.dns_gen")

        # Step 1: Prepare wordlist for dynamic brute
        commands = [
            f"curl -s https://raw.githubusercontent.com/AlephNullSK/dnsgen/master/dnsgen/words.txt -o {dns_gen_words}",
            f"curl -s https://raw.githubusercontent.com/infosec-au/altdns/master/words.txt -o {alt_dns_words}",
            f"cat {dns_gen_words} {alt_dns_words} | sort -u > {merged_path}",
        ]
        for cmd in commands:
            print(f"{Colors.GRAY}Executing command: {cmd}{Colors.RESET}")
            run_command_in_zsh(cmd)

        # Step 2: Get subdomains for dynamic brute
        subdomains = get_subdomains(scope=domain)
        with open(dns_brute, "w") as file:
            file.write("\n".join([f"{sub.subdomain}" for sub in subdomains]))

        command = f"cat {dns_brute} | dnsgen -w {merged_path} - | tee {domain_dns_gen}"
        dns_gen_result = run_command_in_zsh(command)

        if len(dns_gen_result) > 30000000:
            subdomains = get_lives(scope=domain)
            with open(dns_brute, "w") as file:
                file.write("\n".join([f"{sub.subdomain}" for sub in subdomains]))
                run_command_in_zsh(command)

        # Step 3: Run shuffledns
        shuffledns_command = (
            f"shuffledns -list {domain_dns_gen} -d {domain} -r ~/.resolvers "
            f"-m $(which massdns) -mode resolve -t 100 -silent"
        )
        print(f"{Colors.GRAY}Executing command: {shuffledns_command}{Colors.RESET}")
        result = run_command_in_zsh(shuffledns_command)

        return result
