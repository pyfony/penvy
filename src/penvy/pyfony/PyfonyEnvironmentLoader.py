import re
from penvy.poetry.PyprojectLoader import PyprojectLoader


class PyfonyEnvironmentLoader:
    def __init__(
        self,
        pyproject_loader: PyprojectLoader,
    ):
        self._pyproject_loader = pyproject_loader

    def load(self) -> dict:
        pyfony_env_section = self._pyproject_loader.get_section("[pyfony.environment]")
        pyfony_environment = {}
        required_entries = ["python"]
        optional_entries = ["pip", "setuptools", "wheel"]
        allowed_entries = required_entries + optional_entries

        if not pyfony_env_section:
            raise Exception("[pyfony.environment] missing in pyproject.toml")

        for line in pyfony_env_section.splitlines():
            line_without_whitespace = "".join(line.split())
            regex = re.compile(r"(.*)=[\"']([0-9]+(.[0-9]+){0,2})[\"']")
            matches = regex.match(line_without_whitespace)

            if not matches or matches.group(1) not in allowed_entries:
                raise Exception(f"Invalid entry '{line}' in [pyfony.environment], allowed entries are {allowed_entries}")

            name = matches.group(1)
            version = matches.group(2)

            pyfony_environment[name] = {"version": version}

        if "python" not in pyfony_environment:
            raise Exception("python missing in [pyfony.environment]")

        for entry in optional_entries:
            if entry not in pyfony_environment:
                pyfony_environment[entry] = {"version": None}

        return pyfony_environment
