class DependenciesLoader:
    def __init__(
        self,
        poetry_lock_path: str,
    ):
        self._poetry_lock_path = poetry_lock_path

    def load(self) -> dict:
        with open(self._poetry_lock_path, "r") as f:
            poetry_lock = f.read()

        dependencies = {}
        lines = poetry_lock.splitlines()

        for index, line in enumerate(lines):
            if line == "[[package]]":
                package_name = lines[index + 1].split(" = ")[1].strip('"')
                package_version = lines[index + 2].split(" = ")[1].strip('"')
                package_category = lines[index + 4].split(" = ")[1].strip('"')
                dependencies[package_name] = {
                    "version": package_version,
                    "category": package_category,
                }

        return dependencies

    def load_main(self) -> dict:
        dependencies = self.load()

        return {
            key: {
                "version": val["version"],
                "category": val["category"],
            }
            for key, val in dependencies.items()
            if val["category"] == "main"
        }

    def load_dev(self) -> dict:
        dependencies = self.load()

        return {
            key: {
                "version": val["version"],
                "category": val["category"],
            }
            for key, val in dependencies.items()
            if val["category"] == "dev"
        }
