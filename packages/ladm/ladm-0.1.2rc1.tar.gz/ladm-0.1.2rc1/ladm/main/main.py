import logging
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from gaia_sdk.api.GaiaCredentials import HMACCredentials
from gaia_sdk.gaia import Gaia
from rx import operators as ops, pipe

from ladm.main.util.allowed_system_dependencies import get_allowed_system_dependencies
from ladm.main.util.custom_exceptions import LADMError


class LADM:
    logger = logging.getLogger('LADM')

    def __init__(self, input_filepath: str, language: str, output_filepath: str = ""):
        """
        :param input_filepath: File path and name of the skill.yml file containing the dependencies
                               (Or any other file containing dependencies in the correct format)
        :param language: For which language to generate the output, python => requirements.txt, java => .gradle
        :param output_filepath: Optional: File path and name to write the output to a file
        """
        self._allowed_system_dependencies: List[str] = get_allowed_system_dependencies()
        self._input_filepath: str = input_filepath
        self._language: str = language
        self._output_filepath: str = output_filepath
        self._language_libraries: List[List[str]] = []
        self._system_dependencies: List[List[str]] = []
        self._models: List[str] = []

    def generate_dependencies_from_file(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Main method to call from this class. Generates two lists.
        :return: Language library dependencies and system-level dependencies
        """
        with open(self._input_filepath, 'r') as stream:
            try:
                dependencies_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.logger.error(exc)
                raise LADMError(f"The supplied YAML in {self._input_filepath} cannot be parsed.")

            if 'dependencies' not in dependencies_yaml:
                self.logger.warning("\'dependencies\' is not specified in skill.yml.")
                self.logger.warning("No additional dependencies will be installed.")
                return [], [], []

            if 'libraries' in dependencies_yaml['dependencies']:
                self._language_libraries = dependencies_yaml['dependencies']['libraries']
            if 'system' in dependencies_yaml['dependencies']:
                self._system_dependencies = dependencies_yaml['dependencies']['system']
            if 'models' in dependencies_yaml['dependencies']:
                self._models = dependencies_yaml['dependencies']['models']

            return self.generate_for_language(), self.generate_for_system(), self.generate_for_models()

    def generate_for_system(self) -> List[str]:
        """
        :return: list of system-level dependencies as strings possibly including version numbers
        """
        if not self._system_dependencies:
            self.logger.warning("System dependencies are empty.")
            return []

        # Parse dependencies and add them to list
        deps_and_versions: dict[str, Optional[str]] = self.convert_yaml_deps_to_dict(self._system_dependencies)

        # Only use allowed deps (This may be removed from here as it is done in RAIN before this as well)
        set_input_deps = set(deps_and_versions.keys())
        set_allowed_deps = set(self._allowed_system_dependencies)
        set_intersection = set_input_deps & set_allowed_deps
        if len(set_intersection) < len(deps_and_versions):
            self.logger.warning("System dependencies contain entries that are not in the list of allowed dependencies:")
            self.logger.warning(set_input_deps - (set_input_deps & set_allowed_deps))
            self.logger.warning("They are discarded from the process.")

        deps_and_versions = {k: v for k, v in deps_and_versions.items() if k in set_intersection}
        return [f"{k}={v}" if v else k for k, v in deps_and_versions.items()]

    def generate_for_language(self) -> List[str]:
        """
        :return: list of language library dependencies as strings possibly including version numbers
        """
        if not self._language_libraries:
            self.logger.warning("Language library dependencies are empty.")
            return []

        language_libraries_generators = {
            "python": self.generate_for_python,
            "java": self.generate_for_java
        }

        if self._language in language_libraries_generators:
            return language_libraries_generators[self._language]()
        else:
            raise LADMError(f"Language {self._language} is not supported.")

    def generate_for_java(self) -> List[str]:
        """
        :return: list of Java libraries as strings possibly including version numbers
        """
        self.logger.warning("LADM for Java/Gradle libraries is not yet implemented.")
        self.logger.warning(f"Language libraries {self._language_libraries} are discarded from the process.")
        return []

    def generate_for_python(self) -> List[str]:
        """
        :return: list of Python libraries as strings possibly including version numbers
        """
        # Parse libraries and add them to list
        libs_and_versions: Dict[str, Optional[str]] = self.convert_yaml_deps_to_dict(self._language_libraries)

        # Python requirements txt needs == instead of single =.
        # (Others too, but that's not implemented) https://www.python.org/dev/peps/pep-0440/#version-specifiers
        requirements_txt_entries: List[str] = [f"{k}=={v}" if v else k for k, v in libs_and_versions.items()]

        # Write them to file if output path is set
        if self._output_filepath:
            self.write_lines_to_file(requirements_txt_entries)

        return requirements_txt_entries

    @staticmethod
    def convert_yaml_deps_to_dict(deps: List[List[str]]) -> Dict[str, Optional[str]]:
        """
        Goes through the list of dependencies where each entry is a list containing a dependency name and a possible
        version as a second entry, converts it to a dict where the keys a re the dependency names and possible
        values are the version

        :param deps: Parsed YAML input of either the system or language dependencies part of dependencies in skill.yml
        :return: dict where keys are names of packages or libraries, and optional values are versions
        """
        return {dep[0]: dep[1] if (len(dep) > 1) else None for dep in deps}

    def write_lines_to_file(self, lines: List[str]):
        Path('/'.join(self._output_filepath.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
        with open(self._output_filepath, 'w') as f:
            for line in lines:
                f.write(f"{line}\n")

    def generate_for_models(self) -> List[str]:
        """
        :return: list of models as strings in GAIA URI format
        """
        if self._models is None:
            self.logger.warning("Models dependencies are empty.")
            return []
        models: List[str] = self.parse_and_filter_yaml_models_to_list(self._models)
        return models

    @staticmethod
    def parse_and_filter_yaml_models_to_list(models: List[str]) -> List[str]:
        """
        Removes models from the input list if they do not conform to the GAIA URI syntax
        :param models: list of data API GAIA URIs
        :return: filtered list
        """
        # This could be removed from here if it is done in RAIN before this step in the build process
        gaia_uri_pattern = re.compile("^gaia://([^@/]+)/(.*)$")
        return [model for model in models if gaia_uri_pattern.match(model)]

    def download_models(self, output_path: str, model_uris: List[str] = None) -> None:
        """
        Downloads models via the GAIA Data API
        :param output_path: path to where the files are downloaded
        :param model_uris: optional - validated model URIs otherwise the member variable of models is used
        """
        # This is done in the acquisition step right now, TODO: Remove it from here
        api_key = os.getenv("GAIA_API_KEY")
        api_secret = os.getenv("GAIA_API_SECRET")
        if any(v is None for v in [api_key, api_secret]):
            self.logger.error("GAIA API KEY or SECRET not set via environment variables")

        gaia_ref = Gaia.connect("http://localhost:8080", HMACCredentials(api_key, api_secret))

        model_uris_to_use = model_uris
        if not model_uris:
            model_uris_to_use = self._models

        for model_uri in model_uris_to_use:
            data = pipe(ops.first())(gaia_ref.data(model_uri).as_bytes()).run()
            # TODO: Make concurrent?
            # TODO: Save files somewhere so they can used in the build context

