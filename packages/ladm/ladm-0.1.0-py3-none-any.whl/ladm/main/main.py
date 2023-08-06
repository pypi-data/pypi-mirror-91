import logging
import re
import yaml
from pathlib import Path
from typing import Union, Hashable, Any, Dict, List, Optional, Tuple

from ladm.main.util.allowed_system_dependencies import get_allowed_system_dependencies
from ladm.main.util.custom_exceptions import LADMError


class LADM:
    logger = logging.getLogger('LADM')

    def __init__(self, input_filepath: str, language: str, output_filepath: str = ""):
        """
        :param input_filepath: File path and name of the dependencies.yml file
        :param language: For which language to generate the output, python => requirements.txt, java => .gradle
        :param output_filepath: Optional: File path and name to write the output to a file
        """
        self.allowed_system_dependencies: List[str] = get_allowed_system_dependencies()
        self.input_filepath: str = input_filepath
        self.language: str = language
        self.output_filepath: str = output_filepath
        self.language_libraries: Union[Dict[Hashable, Any], List, None] = None
        self.system_dependencies: Union[Dict[Hashable, Any], List, None] = None
        self.models: Union[Dict[Hashable, Any], List, None] = None

    def generate_dependencies_from_file(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Main method to call from this class. Generates two lists.
        :return: Language library dependencies and system-level dependencies
        """
        with open(self.input_filepath, 'r') as stream:
            try:
                dependencies_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.logger.error(exc)
                raise LADMError(f"The supplied YAML in {self.input_filepath} cannot be parsed.")

            try:
                self.language_libraries = dependencies_yaml['dependencies']['libraries']
                self.system_dependencies = dependencies_yaml['dependencies']['system']
                if not self.language_libraries or not self.system_dependencies:
                    raise LADMError(f"'dependencies' or 'libraries' is empty in supplied YAML at {self.input_filepath}")
            except KeyError as exc:
                self.logger.error(exc)
                raise LADMError(
                    f"The supplied YAML in {self.input_filepath} does not contain 'dependencies' or 'libraries'.")

            if 'models' in dependencies_yaml['dependencies']:
                self.models = dependencies_yaml['dependencies']['models']

            return self.generate_for_language(), self.generate_for_system(), self.generate_for_models()

    def generate_for_system(self) -> List[str]:
        """
        :return: list of system-level dependencies as strings possibly including version numbers
        """
        # Parse dependencies and add them to list
        deps_and_versions: dict[str, Optional[str]] = self.convert_yaml_deps_to_dict(self.system_dependencies)

        # Only use allowed deps
        set_input_deps = set(deps_and_versions.keys())
        set_allowed_deps = set(self.allowed_system_dependencies)
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
        language_libraries_generators = {
            "python": self.generate_for_python,
            "java": self.generate_for_java
        }

        if self.language in language_libraries_generators:
            return language_libraries_generators[self.language]()
        else:
            raise LADMError(f"Language {self.language} is not supported.")

    def generate_for_java(self) -> List[str]:
        """
        :return: list of Java libraries as strings possibly including version numbers
        """
        self.logger.warning("LADM for Java/Gradle libraries is not yet implemented.")
        self.logger.warning(f"Language libraries {self.language_libraries} are discarded from the process.")
        return []

    def generate_for_python(self) -> List[str]:
        """
        :return: list of Python libraries as strings possibly including version numbers
        """
        # Parse libraries and add them to list
        libs_and_versions: Dict[str, Optional[str]] = self.convert_yaml_deps_to_dict(self.language_libraries)

        # Python requirements txt needs == instead of single =.
        # (Others too, but that's not implemented) https://www.python.org/dev/peps/pep-0440/#version-specifiers
        requirements_txt_entries: List[str] = [f"{k}=={v}" if v else k for k, v in libs_and_versions.items()]

        # Write them to file if output path is set
        if self.output_filepath:
            self.write_lines_to_file(requirements_txt_entries)

        return requirements_txt_entries

    @staticmethod
    def convert_yaml_deps_to_dict(deps: Union[Dict[Hashable, Any], List, None]) -> Dict[str, Optional[str]]:
        """
        :param deps: Parsed YAML input of either the system or language dependencies part of dependencies.yml
        :return: dict where keys are names of packages or libraries, and optional values are versions
        """
        entries: Dict[str, Optional[str]] = {}
        for dep in deps:
            if isinstance(dep, dict):
                LADM.logger.info(f"Found versioned dependency: {dep}")
                dep_name, version = list(dep.items())[0]
                if version is None:
                    raise LADMError(f"Unrecognized dependency syntax format: {dep}")
                entries[dep_name] = version

            elif isinstance(dep, str):
                LADM.logger.info(f"Found unversioned dependency: {dep}")
                entries[dep] = None

            else:
                raise LADMError(f"Unrecognized dependency syntax format: {dep}")

        return entries

    def write_lines_to_file(self, lines: List[str]):
        Path('/'.join(self.output_filepath.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
        with open(self.output_filepath, 'w') as f:
            for line in lines:
                f.write(f"{line}\n")

    def generate_for_models(self) -> List[str]:
        if self.models is None:
            return []
        models: List[str] = self.parse_and_filter_yaml_models_to_list(self.models)
        return models

    @staticmethod
    def parse_and_filter_yaml_models_to_list(models: Union[Dict[Hashable, Any], List, None]) -> List[str]:
        gaia_uri_pattern = re.compile("^gaia://([^@/]+)/(.*)$")
        models_list = []
        for model in models:
            if not gaia_uri_pattern.match(model):
                LADM.logger.warning(f"Model {model} does not match the GAIA URI format, it is discarded.")
                continue
            models_list.append(model)
        return models_list

