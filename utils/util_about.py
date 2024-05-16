"""
======================= INSTRUCTOR-GENERATED FILE =============================
Source: https://github.com/denisecase/nw-diagnostics-python/
================================================================================

PURPOSE:
- Generate information about the local machine and Python installation.
- Help detect common issues.

NO WORRIES:
- This is NOT part of your project tasks. It's here to help.
- As an instructor-provided script, there's no need to modify or delve 
  into its internals. 

NO EXTERNAL DEPENDENCIES:
- This script uses ONLY modules included in the Python standard library.
- No installations (besides Python) are required.

USAGE:
To use, execute this script. In VS Code select Terminal / New Terminal and 
run the following command: python util_about.py
- OR On Windows:         py util_about.py
- OR On macOS/Linux:     python3 util_about.py

@Author: Denise Case
@Updated: 2021-08

==========================================================================
"""

# Import from Python Standard Library

import datetime
import os
import platform
import shutil
import sys

# Declare program constants (typically constants are named with ALL_CAPS)

DIVIDER = "=" * 70  # A string divider for cleaner output formatting
OUTPUT_FILENAME = "util_about.txt"  # File name for saving the info

# Retrieve additional system information using platform and os modules

build_date, compiler = platform.python_build()
implementation = platform.python_implementation()
architecture = platform.architecture()[0]
user_home = os.path.expanduser("~")

# Define program functions (bits of reusable code)


def get_terminal_info():
    """Determine the terminal and environment."""
    term_program = os.environ.get("TERM_PROGRAM", "")
    term_program_version = os.environ.get("TERM_PROGRAM_VERSION", "").lower()

    if term_program == "vscode":
        environment = "VS Code"
        if "powershell" in term_program_version:
            current_shell = "powershell"
        else:
            # Fallback approach for VS Code
            current_shell = (
                os.environ.get("SHELL", os.environ.get("ComSpec", ""))
                .split(os.sep)[-1]
                .lower()
            )
    else:
        environment = "Native Terminal"
        current_shell = (
            os.environ.get("SHELL", os.environ.get("ComSpec", ""))
            .split(os.sep)[-1]
            .lower()
        )

    return environment, current_shell


def get_source_directory_path():
    """
    Returns the absolute path to the directory containing this script.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    return dir


def is_git_in_path():
    """
    Checks if git is available in the PATH.

    Returns:
    - bool: True if git is in the PATH, otherwise False.
    """
    return shutil.which("git") is not None


def get_preferred_command():
    """
    Determine the preferred Python command based on the operating system.

    Returns:
    - str: 'python' for Windows, 'python3' for macOS and Linux.
    """
    if os.name == "nt":  # Checks if the OS is Windows.
        return "python"
    return "python3"


def is_preferred_command_available():
    """
    Checks if the preferred Python command is available in the PATH.

    Returns:
    - tuple: (str: Preferred command name, bool: Availability in PATH)
    """
    preferred_command = get_preferred_command()
    is_available = shutil.which(preferred_command) is not None
    return is_available


def print_info_to_file(filename, content):
    """
    Print the provided content to a specified file.

    Args:
    - filename (str): Name of the file to save the content in.
    - content (str): The content to save.
    """
    with open(filename, "w") as f:
        f.write(content)


def get_header(fn):
    """
    Constructs a formatted string that provides helpful information.

    Args:
    - fn (str): Path to the file for which the information should be generated.

    Returns:
    - str: Formatted debug information.
    """

    environment, current_shell = get_terminal_info()

    return f"""
{DIVIDER}
{DIVIDER}
 Welcome to the NW Python Debugging Information Utility!
 Date and Time: {datetime.date.today()} at {datetime.datetime.now().strftime("%I:%M %p")}
 Operating System: {os.name} {platform.system()} {platform.release()}
 System Architecture: {architecture}
 Number of CPUs: {os.cpu_count()}
 Machine Type: {platform.machine()}
 Python Version: {platform.python_version()}
 Python Build Date and Compiler: {build_date} with {compiler}
 Python Implementation: {implementation}
 Active pip environment:   {os.environ.get('PIP_DEFAULT_ENV', 'None')}
 Active conda environment: {os.environ.get('PIP_DEFAULT_ENV', 'None')}
 Path to Interpreter:         {sys.executable}
 Path to virtual environment: {sys.prefix}
 Current Working Directory:   {os.getcwd()}
 Path to source directory:    {get_source_directory_path()}
 Path to script file:         {fn}
 User's Home Directory:       {user_home}
 Terminal Environment:        {environment}
 Terminal Type:               {current_shell}
 Preferred command:           {get_preferred_command()}
 Is {get_preferred_command()} available in PATH:   {is_preferred_command_available()}
 Is git available in PATH:      {is_git_in_path()} 
{DIVIDER}
{DIVIDER}
"""


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # We are using the get_header function and providing it with the path to this script.
    # This will generate the debug information for the current script.
    debug_info = get_header(__file__)

    # Print the debug information to the console.
    print(debug_info)

    # Print the debug information to a file named by the value in OUTPUT_FILENAME.
    print_info_to_file(OUTPUT_FILENAME, debug_info)
