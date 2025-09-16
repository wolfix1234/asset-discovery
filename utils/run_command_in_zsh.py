# utils/shell_utils.py
import subprocess

def run_command_in_zsh(command, read_line=True):
    try:
        result = subprocess.run(["zsh", "-c", command], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error occurred:", result.stderr)
            return False
        if read_line:
            return result.stdout.splitlines()
        return result.stdout
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
