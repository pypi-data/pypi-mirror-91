import logging
import subprocess
import sys
import os


def get_logger(level="INFO"):
    level = {
        "ERROR": logging.ERROR,
        "WARN": logging.WARN,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }[level]

    formatter = logging.Formatter(
        fmt="%(asctime)s — %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def _validate_base_directory(cwd):
    if not os.path.exists(cwd + "/idk.json"):
        sys.exit(
            "No idk.json in current working directory, are you in the base directory of your insight?")


def _lint_directory(cwd, logger):
    has_error = False
    for root, _, f_names in os.walk(cwd):
        if ".venv" in root:
            continue
        for fn in f_names:
            if not fn.endswith(".py"):
                continue
            path = root + "/" + fn
            type_hint_cmd = f'mypy --ignore-missing-imports {path}'.split()
            for return_path in _execute_iterator(type_hint_cmd):
                if "error" in return_path and not "source file" in return_path:
                    has_error = True
                    logger.error(return_path.strip())
    return has_error


def _execute_iterator(cmd, err_out=False):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code and err_out:
        raise subprocess.CalledProcessError(return_code, cmd)
