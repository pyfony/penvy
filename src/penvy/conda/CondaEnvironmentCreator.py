import os
import tempfile
import urllib.request
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.pyfony.PyfonyEnvironmentLoader import PyfonyEnvironmentLoader
from penvy.shell.runner import run_shell_command


class CondaEnvironmentCreator(SetupStepInterface):
    def __init__(
        self,
        conda_executable_path: str,
        venv_dir: str,
        pyfony_environment_loader: PyfonyEnvironmentLoader,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._venv_dir = venv_dir
        self._pyfony_environment_loader = pyfony_environment_loader
        self._logger = logger

    def get_description(self):
        return "Create the project conda environment"

    def run(self):
        self._logger.info(f"Creating Conda environment in {self._venv_dir}")

        self._create_conda_env()

        self._logger.info(f"Installing pip, setuptools, wheel in {self._venv_dir}")

        self._install_base_python_packages()

    def should_be_run(self) -> bool:
        return not os.path.isdir(self._venv_dir)

    def _create_conda_env(self):
        pyfony_environment = self._pyfony_environment_loader.load()
        python_version = pyfony_environment["python"]["version"]

        run_shell_command(
            f"{self._conda_executable_path} create "
            f"-y -c conda-forge --override-channels --no-deps --no-default-packages "
            f"-p {self._venv_dir} python={python_version}",
            shell=True,
        )

    def _install_base_python_packages(self):
        pyfony_environment = self._pyfony_environment_loader.load()
        packages = ["pip", "setuptools", "wheel"]
        args = [f"{package}=={pyfony_environment[package]['version']}" for package in packages if pyfony_environment[package]["version"]]
        args += ["--no-warn-script-location"]

        url = "https://bootstrap.pypa.io/get-pip.py"
        temp_dir = tempfile.mkdtemp()
        pip_bootstrap_script_path = f"{temp_dir}/get-pip.py"
        urllib.request.urlretrieve(url, pip_bootstrap_script_path)

        run_shell_command(f"{self._venv_dir}/python {pip_bootstrap_script_path} {' '.join(args)}", shell=True)
