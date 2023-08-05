"""Python Developer eXperience (PyDx) console application installation."""
import pathlib
import setuptools


def is_pip_compile_noise(line_of_requirements_file):
    return any(
        [
            line_of_requirements_file.startswith(" "),
            line_of_requirements_file.startswith("#"),
            line_of_requirements_file.startswith("-"),
        ]
    )


with pathlib.Path("README.rst").open() as readme_file:
    package_description = readme_file.read()

with pathlib.Path("CHANGELOG.md").open() as changelog_file:
    package_description += f"\n\n{changelog_file.read()}"

with pathlib.Path("requirements", "production.txt").open() as requirements_file:
    requirements = [
        line.strip()
        for line in requirements_file.readlines()
        if not is_pip_compile_noise(line)
    ]

setuptools.setup(
    entry_points={
        "console_scripts": ("pydx = pydx.main:cli",),
    },
    install_requires=requirements,
    long_description=package_description,
    packages=setuptools.find_packages(include=["pydx", "pydx.*"]),
)
