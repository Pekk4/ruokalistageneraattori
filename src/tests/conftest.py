from os import mkdir
from shutil import rmtree


def pytest_sessionstart():
    mkdir("test_logs")

def pytest_sessionfinish():
    rmtree("test_logs/", ignore_errors=True)
