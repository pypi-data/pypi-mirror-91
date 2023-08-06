from typing import List, Union

LanguageDependenciesInput = List[List[str]]
SystemDependenciesInput = List[List[str]]
ModelsDependenciesInput = List[str]
DependenciesInput = Union[LanguageDependenciesInput, SystemDependenciesInput, ModelsDependenciesInput]

LanguageDependenciesOutput = List[str]
SystemDependenciesOutput = List[str]
ModelsDependenciesOutput = List[str]
DependenciesOutput = Union[LanguageDependenciesOutput, SystemDependenciesOutput, ModelsDependenciesOutput]
