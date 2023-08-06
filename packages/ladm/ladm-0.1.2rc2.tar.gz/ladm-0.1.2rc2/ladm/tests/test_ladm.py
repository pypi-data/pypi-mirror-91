import shutil
import unittest
from pathlib import Path
from ladm.main.main import LADM
from ladm.main.util.custom_exceptions import LADMError


class LADMTestCase(unittest.TestCase):
    default_output_path = "test-output/LADM"
    default_output_file_name = "LADM-requirements.txt"

    def tearDown(self) -> None:
        if Path(self.default_output_path).exists():
            shutil.rmtree(self.default_output_path.split('/')[0])

    def test_correct_illegal_dependency_filtering(self) -> None:
        dependencies_yml_path = "resources/correct-skill-ladm/skill_with_dependencies.yml"
        ladm = LADM(dependencies_yml_path,
                    "python", str(Path(self.default_output_path) / self.default_output_file_name))
        results = ladm.generate_dependencies_from_file()
        self.assertTrue((Path(self.default_output_path) / self.default_output_file_name).exists())

        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          []), results)

    def test_no_dependencies(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_without_dependencies.yml",
                    "python")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual(([], [], []), results)

    def test_empty_dependencies(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_with_dependencies_empty.yml",
                    "python")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual(([], [], []), results)

    def test_system_dependencies_only(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_with_dependencies_system_only.yml",
                    "python")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual(([],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          []), results)

    def test_libraries_only(self) -> None:
        ladm = LADM("resources/correct-skill-ladm/skill_with_dependencies_libraries_only.yml",
                    "python")
        results = ladm.generate_dependencies_from_file()
        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          [],
                          []), results)

    def test_correct_models(self) -> None:
        dependencies_yml_path = "resources/correct-skill-ladm/skill_with_dependencies_with_models.yml"
        ladm = LADM(dependencies_yml_path,
                    "python", str(Path(self.default_output_path) / self.default_output_file_name))
        results = ladm.generate_dependencies_from_file()
        self.assertEqual((["zupline==1.0.0", "tensorblow"],
                          ["libffi-dev", "default-jre=2:1.11-71"],
                          ["gaia://tenant/a.txt", "gaia://tenant/test/b.txt"]), results)
