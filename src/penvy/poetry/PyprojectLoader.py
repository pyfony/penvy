class PyprojectLoader:
    def __init__(
        self,
        pyproject_path: str,
    ):
        self._pyproject_path = pyproject_path

    def load_pyproject(self) -> str:
        with open(self._pyproject_path, "r") as f:
            return self._remove_comments(f.read())

    def get_section(self, section_start: str) -> str:
        pyproject_toml = self.load_pyproject()
        section = ""
        in_section = False

        for line in pyproject_toml.splitlines():
            if line.strip().startswith(section_start):
                in_section = True
                continue

            if in_section and line.strip().startswith("["):
                break

            if in_section and line.strip() != "":
                section += line + "\n"

        return section

    def _remove_comments(self, pyproject_toml: str) -> str:
        pyproject_without_comments = ""

        for line in pyproject_toml.splitlines():
            index = line.find("#")

            if index >= 0:
                pyproject_without_comments += line[0:index] + "\n"

            else:
                pyproject_without_comments += line + "\n"

        return pyproject_without_comments
