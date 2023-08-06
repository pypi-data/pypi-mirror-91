import logging
import yaml
from typing import List, Tuple

from ladm.main.GeneratorContext import GeneratorContext
from ladm.main.GeneratorStrategy import LanguageGeneratorStrategy, SystemGeneratorStrategy, ModelGeneratorStrategy
from ladm.main.util.allowed_system_dependencies import get_allowed_system_dependencies
from ladm.main.util.custom_exceptions import LADMError
from ladm.main.util.types import LanguageDependenciesOutput, SystemDependenciesOutput, ModelsDependenciesOutput


class LADM:
    logger = logging.getLogger('LADM')

    def __init__(self, input_filepath: str, language: str = None):
        """
        :param input_filepath: File path and name of the skill.yml file containing the dependencies
                               (Or any other file containing dependencies in the correct format)
        :param language: For which language to generate the output, python => requirements.txt format, java => .gradle
        """
        self._allowed_system_dependencies: List[str] = get_allowed_system_dependencies()
        self._input_filepath: str = input_filepath
        self._language: str = language

    def generate_dependencies_from_file(self,
                                        do_language: bool = True,
                                        do_system: bool = True,
                                        do_models: bool = True) -> Tuple[LanguageDependenciesOutput,
                                                                         SystemDependenciesOutput,
                                                                         ModelsDependenciesOutput]:
        """
        Main method to call from this class. Generates three lists.
        :param do_language: generate language libraries dependencies
        :param do_system: generate system dependencies
        :param do_models: generate model dependencies
        :return: Language library dependencies, system-level dependencies, model dependencies
        """
        self.logger.info(f"Generating with args{list(vars().items())[1:]} and language {self._language}")

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

            language_libraries = dependencies_yaml['dependencies'].get('libraries')
            system_dependencies = dependencies_yaml['dependencies'].get('system')
            models = dependencies_yaml['dependencies'].get('models')

            language_libraries_results: LanguageDependenciesOutput = []
            system_dependencies_results: SystemDependenciesOutput = []
            models_results: ModelsDependenciesOutput = []

            context = GeneratorContext()
            if do_language:
                context.strategy = LanguageGeneratorStrategy(self._language)
                language_libraries_results = context.execute_strategy(language_libraries)
            if do_system:
                context.strategy = SystemGeneratorStrategy()
                system_dependencies_results = context.execute_strategy(system_dependencies)
            if do_models:
                context.strategy = ModelGeneratorStrategy()
                models_results = context.execute_strategy(models)

            return language_libraries_results, system_dependencies_results, models_results
