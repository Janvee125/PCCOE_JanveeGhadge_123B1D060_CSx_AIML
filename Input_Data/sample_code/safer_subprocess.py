import subprocess


def check_status():
    result = subprocess.run(
        ["git", "status"],
        shell=False,
        capture_output=True,
        text=True,
        check=False
    )
    return result.stdout
