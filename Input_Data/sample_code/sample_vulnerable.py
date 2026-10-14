import subprocess

PASSWORD = "demo-password-do-not-use"

def run_command(user_input):
    # Demonstration only: passing user input to a shell can be dangerous.
    return subprocess.call(user_input, shell=True)

def get_item(items, index):
    return items[index]
