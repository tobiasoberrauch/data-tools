import subprocess

def run(command: str) -> None:
    """Runs a command in the terminal"""
    subprocess.run(command, shell=True)


def dev() -> None:
    """Runs the development server"""
    run("uvicorn --factory data_tools.main:create_app --reload")