"""
======================= INSTRUCTOR-GENERATED FILE =======================

This is an auxiliary script designed to assist you in verifying the virtual 
environment setup for your project. It is NOT part of the main project tasks.

You do NOT need to understand every detail or modify this file. 

Before diving into the main project, run this script. 
It will diagnose your environment, log results to the terminal, and save 
them in a file named `aboutenv.txt`. 
If you face issues with your environment setup, review this file and share 
its contents to help with debugging.

This script uses ONLY modules included in the Python standard library.
No additional installations are required.

USAGE:
To use, execute this script. In VS Code select Terminal / New Terminal and 
run the following command: python util_aboutenv.py
- OR On Windows:         py util_aboutenv.py
- OR On macOS/Linux:     python3 util_aboutenv.py

@Author: Denise Case
@Updated: 2023-08

==========================================================================

"""

# Import from Python Standard Library

import datetime
import logging
import os
import sys

# Setup logging

OUTPUT_FILENAME = "aboutenv.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.FileHandler(OUTPUT_FILENAME, mode="w"), logging.StreamHandler()],
)

# Declare additional program constants

DIVIDER = "=" * 70  # A string divider for cleaner output formatting
CREATE_COMMAND = "python -m venv .venv"
ACTIVATE_COMMAND_WINDOWS = ".venv\\Scripts\\activate"
ACTIVATE_COMMAND_MAC_LINUX = "source .venv/bin/activate"
UPGRADE_COMMAND = "python -m pip install --upgrade pip"
INSTALL_COMMAND = "python -m pip install"
SUCCESS_MESSAGE = "All checks passed successfully! Your environment is set up correctly.\nIf it asks you to upgrade pip, please do so using the suggested command."


# Define program functions (bits of reusable code)


def get_activate_command():
    """Returns the command to activate the virtual environment."""
    if sys.platform == "win32":
        return ACTIVATE_COMMAND_WINDOWS
    else:
        return ACTIVATE_COMMAND_MAC_LINUX


def check_for_dotvenv_folder():
    """Checks if the .venv folder exists."""
    if os.path.exists(".venv"):
        error_code = 0
        message = "YAY! .venv directory exists."
    else:
        error_code = 1
        message = f"ERROR: Missing .venv directory. Create it (may take a while) using: {CREATE_COMMAND}"
    return error_code, message


def check_dotvenv_is_active():
    """Checks if the .venv virtual environment is active."""
    venv_path = os.environ.get(".venv")

    if venv_path and ".venv" in venv_path:
        error_code = 0
        message = "YAY! The .venv virtual environment is active."
    else:
        ACTIVATE_COMMAND = get_activate_command()
        error_code = 1
        message = (
            f"ERROR: Activate the .venv virtual environment using: {ACTIVATE_COMMAND}"
        )
    return error_code, message


def get_search_path_string():
    paths = "\n".join(sys.path)
    return f"""
Python's package search paths:
{"-" * 40}
{paths}
{"-" * 40}
"""


def read_dependencies():
    """Read dependencies from requirements.txt and return a list of package names."""
    dependency_list = []
    if not os.path.exists("requirements.txt"):
        logging.warning("No requirements.txt file found.")
        return dependency_list

    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            # Split on the first occurrence of the comparison operator to retrieve the package name
            package_name = line.split("==")[0].strip()
            dependency_list.append(package_name)

    return dependency_list


def check_dependencies_installed_in_dotvenv():
    """Checks if dependencies are installed in the virtual environment."""
    # Show all the places Python will look for packages
    logging.debug(get_search_path_string())

    DEPENDENCIES_LIST = read_dependencies()

    for dependency in DEPENDENCIES_LIST:
        try:
            __import__(dependency)
        except ImportError as e:
            logging.error(e)
            message = f"ERROR: {dependency} is not installed in .venv. Install it by running: {INSTALL_COMMAND} {dependency}"
            return (1, message)

    # Only reach this point if all dependencies are installed
    message = "YAY! All dependencies are installed in the .venv."
    return 0, message


def log_with_divider(message):
    """Logs a message and the DIVIDER."""
    logging.info(message)
    logging.info(DIVIDER)


def verify_environment():
    """Verify the environment step by step."""

    log_with_divider(f"{DIVIDER}")

    checks = [
        check_for_dotvenv_folder,
        check_dotvenv_is_active,
        check_dependencies_installed_in_dotvenv,
    ]

    for check in checks:
        error_code, message = check()
        log_with_divider(message)

        # If the error code exists (is not zero), then exit the program
        if error_code:
            sys.exit()

    log_with_divider(f"\n{SUCCESS_MESSAGE}\n")


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.info(DIVIDER)
    logging.info("Welcome to the Python Debugging Information Utility ABOUTENV.PY")
    logging.info(
        f"Date and Time: {datetime.date.today()} at {datetime.datetime.now().strftime('%I:%M %p')}"
    )
    verify_environment()
