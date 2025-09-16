import os
import tempfile

from utils import run_command_in_zsh


class Colors:
    GRAY = "\033[90m"
    RESET = "\033[0m"


def static_brute(domain):
    # Paths for temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        best_dns_path = os.path.join(temp_dir, "best-dns-wordlist.txt")
        subdomains_path = os.path.join(temp_dir, "2m-subdomains.txt")
        crunch_path = os.path.join(temp_dir, "4-lower.txt")
        static_words_path = os.path.join(temp_dir, "static-finals.txt")
        domain_static_path = os.path.join(temp_dir, f"{domain}.static")

        # Step 1: Prepare wordlist for static brute
        commands = [
            f"curl -s https://wordlists-cdn.assetnote.io/data/manual/best-dns-wordlist.txt -o {best_dns_path}",
            f"curl -s https://wordlists-cdn.assetnote.io/data/manual/2m-subdomains.txt -o {subdomains_path}",
            f"crunch 1 4 abcdefghijklmnopqrstuvwxyz1234567890 > {crunch_path}",
            f"cat {best_dns_path} {subdomains_path} {crunch_path} | sort -u > {static_words_path}",
            f"awk -v domain='{domain}' '{{print $0\".\"domain}}' {static_words_path} > {domain_static_path}",
        ]
        for cmd in commands:
            print(f"{Colors.GRAY}Executing command: {cmd}{Colors.RESET}")
            run_command_in_zsh(cmd)

        # Step 2: Run shuffledns
        shuffledns_command = (
            f"shuffledns -list {domain_static_path} -d {domain} -r ~/.resolvers "
            f"-m $(which massdns) -mode resolve -t 100 -silent"
        )
        print(f"{Colors.GRAY}Executing command: {shuffledns_command}{Colors.RESET}")
        result = run_command_in_zsh(shuffledns_command)

        return result
