from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_shell_command


class DependenciesInstaller(SetupStepInterface):
    def __init__(
        self,
        poetry_executable_path: str,
        verbose_output_enabled: bool,
        logger: Logger,
    ):
        self._poetry_executable_path = poetry_executable_path
        self._verbose_output_enabled = verbose_output_enabled
        self._logger = logger

    def get_description(self):
        return "Install all python dependencies"

    def run(self):
        self._logger.info("Installing dependencies from poetry.lock")

        cmd_parts = [
            self._poetry_executable_path,
            "install",
            "--no-root",
        ]

        if self._verbose_output_enabled:
            cmd_parts.append("-vvv")

        run_shell_command(" ".join(cmd_parts), shell=True)

    def should_be_run(self) -> bool:
        return True
