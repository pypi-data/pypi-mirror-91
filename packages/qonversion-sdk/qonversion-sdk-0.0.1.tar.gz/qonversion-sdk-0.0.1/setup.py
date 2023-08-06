import os
import sys
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = "-n auto --color=yes"

    def run_tests(self):
        import shlex

        # import pytest inside method, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


current_folder = os.path.abspath(os.path.dirname(__file__))

os.chdir(current_folder)

version_contents = {}
with open(
    os.path.join(current_folder, "qonversion", "version.py"), encoding="utf-8"
) as f:
    exec(f.read(), version_contents)

with open(os.path.join(current_folder, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="qonversion-sdk",
    version=version_contents["VERSION"],
    description="Python bindings for the Qonversion API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="qonversion",
    author_email="hi@qonversion.io",
    url="https://github.com/qonversion/python-sdk",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=['requests >= 2.20; python_version >= "3.6"'],
    python_requires=">=3.6",
    tests_require=[
        "pytest >= 6.0.0",
        "pytest-mock >= 2.0.0",
        "pytest-xdist >= 1.31.0",
        "pytest-cov >= 2.8.1",
        "coverage >= 4.5.3",
    ],
    cmdclass={"test": PyTest},
    project_urls={"Source Code": "https://github.com/qonversion/python-sdk"},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
