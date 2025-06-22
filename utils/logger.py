"""
How It Works:
#     logger.info("This is an info message.")
#     logger.warning("This is a warning message.")
#     logger.error("This is an error message.")

* Logs Directory:
The code uses os.path.join(os.getcwd(), "logs") to create a folder called logs in project’s root directory.
The os.makedirs(..., exist_ok=True) call ensures the folder exists without raising an error if it already does.

* Date Formatting:
The current date is formatted using datetime.now().strftime("%d_%m_%Y"),
which produces a string for example 29_01_2025.

* Determining the Test Suite Name:
The code loops over sys.argv looking for a command-line argument that ends with .py.
If found, it uses that file’s base name (without the extension) as part of the log file name.
If none is found, it defaults to "default".

* Log File Naming:
The log file is named by combining the test suite name and date (for example, test_login_29_01_2025.log).
Log file is placed in directory: project_name\logs\...

* Logging Configuration:
The logging.basicConfig(...) call sets up the logging level, format, and handlers.
It uses both a FileHandler (to write logs to the file) and a StreamHandler (to print logs to the console).

Usage Example in conftest.py or Tests:
In conftest.py, we can simply import and use the logger like this:
------------------------------------------------------------------
import:
from utils.logger import logger  # 'logger' is a global object
use:
logger.info("Logging is configured and ready for use.")
------------------------------------------------------------------
"""
import logging
import os
import sys
from datetime import datetime


def setup_logging(log_level=logging.INFO):
    """
    NOTE: change the log details level with -> log_level=logging.INFO
    levels:
    DEBUG > INFO > WARNING > ERROR > FATAL

    Configures logging for the entire project.
    - Ensures logs are saved in the "logs" directory.
    - The log file name is based on the test suite file that was run (if available)
      and the current date (formatted as dd_mm_yyyy).
    - If no test suite file is found in sys.argv, defaults to 'default'.
    This function also clears any existing logging handlers so that the new configuration is applied.
    """
    # Remove any existing handlers on the root logger.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create the logs directory in the project root.
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Try to extract the test suite filename from sys.argv (e.g., "test_login.py")
    test_suite_name = "combined_suites"  # default
    for arg in sys.argv:
        if arg.endswith(".py"):
            # Extract the basename (e.g., test_login)
            test_suite_name = os.path.basename(arg)
            # remove redundant parts
            test_suite_name = test_suite_name.replace(".py", "")
            test_suite_name = test_suite_name.replace("test_", "")
            break

    current_date = datetime.now().strftime("%d_%m_%Y")
    # Construct the log file name, e.g., test_login_29_01_2025.log
    log_file_name = f"{test_suite_name}_{current_date}.log"
    log_file = os.path.join(logs_dir, log_file_name)

    # Configure logging: both to file and console.
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",  # This removes the milliseconds
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    # Return a logger instance for this module (or use logging.getLogger() for the root logger)
    return logging.getLogger(__name__)


# Create a global logger instance.
logger = setup_logging() # AUTO INITIALIZED when module imported



# ====================================================================================================================
# def setup_logging(log_level=logging.INFO):
#     """
#     Configures logging for the entire project.
#
#     - Ensures logs are saved in the "logs" directory.
#     - The log file name is based on a test suite file name if a single file is executed,
#       otherwise it defaults to "combined" when multiple test files are run.
#     - The filename also includes the current date (formatted as dd_mm_yyyy).
#     - Any existing logging handlers are removed before configuration.
#     """
#     # Remove any existing handlers on the root logger.
#     for handler in logging.root.handlers[:]:
#         logging.root.removeHandler(handler)
#
#     # Create the logs directory at the project root.
#     logs_dir = os.path.join(os.getcwd(), "logs")
#     os.makedirs(logs_dir, exist_ok=True)
#
#     # Gather all command-line arguments that end with '.py'
#     test_suite_files = [arg for arg in sys.argv if arg.endswith(".py")]
#
#     # If exactly one test file is specified, use its name; otherwise, default to 'combined'
#     if len(test_suite_files) == 1:
#         test_suite_name = os.path.basename(test_suite_files[0]).replace(".py", "").replace("test_", "")
#     else:
#         test_suite_name = "combined"
#
#     # Get the current date in the format "dd_mm_yyyy"
#     current_date = datetime.now().strftime("%d_%m_%Y")
#     # Construct the log file name, e.g., "login_29_01_2025.log" or "combined_29_01_2025.log"
#     log_file_name = f"{test_suite_name}_{current_date}.log"
#     log_file = os.path.join(logs_dir, log_file_name)
#
#     # Configure logging: output both to file and console.
#     logging.basicConfig(
#         level=log_level,
#         format="%(asctime)s [%(levelname)s] %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",  # No milliseconds
#         handlers=[
#             logging.FileHandler(log_file),
#             logging.StreamHandler()
#         ]
#     )
#     # Return a logger instance for this module.
#     return logging.getLogger(__name__)

# ====================================================================================================================

# def setup_logging(log_level=logging.INFO):
#     """
#     Configures logging for the entire project.
#     Log messages are saved in the "logs" directory with the test suite filename and date.
#     """
#     # Create the logs directory at the project root if it doesnt already exist
#     logs_dir = os.path.join(os.getcwd(), "logs")
#     os.makedirs(logs_dir, exist_ok=True)
#
#     # Derive log file name based on the test suite name and date
#     current_date = datetime.now().strftime("%d_%m_%Y")
#     log_file = os.path.join(logs_dir, f"test_logs_{current_date}.log")
#
#     # Configure logging
#     logging.basicConfig(
#         level=log_level,
#         format="%(asctime)s [%(levelname)s]: %(message)s",
#         handlers=[
#             logging.FileHandler(log_file),
#             logging.StreamHandler()
#         ]
#     )
#     return logging.getLogger(__name__)
#
#
# # Create a global logger instance
# logger = setup_logging()

# ====================================================================================================================

