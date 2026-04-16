import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from click.testing import CliRunner

import xnat_dcm2bids.lobi_scripts as lobi_scripts_module


def run_git(args, cwd):
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


class LobiScriptsTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.tmp_path = Path(self.temp_dir.name)

    def test_intro_without_arguments(self):
        result = self.runner.invoke(lobi_scripts_module.lobi_scripts, [])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Scripts from the lobi-mri-scripts GitHub repository", result.output)
        self.assertIn("lobi_scripts add <script_name> [destination]", result.output)
        self.assertIn("lobi_scripts diff <local_copy> [remote_script_name]", result.output)

    def test_ls_lists_top_level_and_nested_scripts(self):
        scripts_dir = self.tmp_path / "lobi-mri-scripts"
        scripts_dir.mkdir()
        (scripts_dir / "top.sh").write_text("#!/bin/bash\necho top\n")
        nested_dir = scripts_dir / "nested"
        nested_dir.mkdir()
        (nested_dir / "child.sh").write_text("#!/bin/bash\necho child\n")

        with patch.object(lobi_scripts_module, "SCRIPTS_DIR", scripts_dir):
            result = self.runner.invoke(lobi_scripts_module.lobi_scripts, ["ls"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("top.sh", result.output)
        self.assertIn("nested/child.sh", result.output)

    def test_add_copies_script_to_selected_directory(self):
        scripts_dir = self.tmp_path / "lobi-mri-scripts"
        scripts_dir.mkdir()
        source_script = scripts_dir / "nested" / "child.sh"
        source_script.parent.mkdir()
        source_script.write_text("#!/bin/bash\necho child\n")
        destination_dir = self.tmp_path / "workspace"

        with patch.object(lobi_scripts_module, "SCRIPTS_DIR", scripts_dir):
            result = self.runner.invoke(
                lobi_scripts_module.lobi_scripts,
                ["add", "nested/child.sh", str(destination_dir)],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertTrue((destination_dir / "child.sh").exists())
        self.assertIn("Copied nested/child.sh", result.output)

    def test_diff_reports_identical_files(self):
        scripts_dir = self.tmp_path / "lobi-mri-scripts"
        scripts_dir.mkdir()
        remote_script = scripts_dir / "run_mriqc.sh"
        remote_script.write_text("#!/bin/bash\necho same\n")
        local_script = self.tmp_path / "run_mriqc.sh"
        local_script.write_text("#!/bin/bash\necho same\n")

        with patch.object(lobi_scripts_module, "SCRIPTS_DIR", scripts_dir):
            result = self.runner.invoke(
                lobi_scripts_module.lobi_scripts,
                ["diff", str(local_script)],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Files are the same", result.output)

    def test_diff_shows_changes(self):
        scripts_dir = self.tmp_path / "lobi-mri-scripts"
        scripts_dir.mkdir()
        remote_script = scripts_dir / "nested" / "child.sh"
        remote_script.parent.mkdir()
        remote_script.write_text("#!/bin/bash\necho remote\n")
        local_script = self.tmp_path / "child.sh"
        local_script.write_text("#!/bin/bash\necho local\n")

        with patch.object(lobi_scripts_module, "SCRIPTS_DIR", scripts_dir):
            result = self.runner.invoke(
                lobi_scripts_module.lobi_scripts,
                ["diff", str(local_script), "nested/child.sh"],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("-echo local", result.output)
        self.assertIn("+echo remote", result.output)

    def test_install_clones_repository(self):
        origin_dir = self.tmp_path / "origin"
        origin_dir.mkdir()
        run_git(["init", "-b", "main"], origin_dir)
        run_git(["config", "user.name", "Codex Test"], origin_dir)
        run_git(["config", "user.email", "codex@example.com"], origin_dir)
        (origin_dir / "run_mriqc.sh").write_text("#!/bin/bash\necho origin\n")
        run_git(["add", "."], origin_dir)
        run_git(["commit", "-m", "initial"], origin_dir)

        scripts_dir = self.tmp_path / "home" / "lobi-mri-scripts"

        with patch.object(lobi_scripts_module, "GITHUB_REPO_URL", str(origin_dir)):
            with patch.object(lobi_scripts_module, "SCRIPTS_DIR", scripts_dir):
                result = self.runner.invoke(lobi_scripts_module.lobi_scripts, ["install"])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue((scripts_dir / "run_mriqc.sh").exists())
        self.assertIn("Scripts cloned", result.output)

    def test_update_stashes_local_changes_and_pulls_remote_commit(self):
        origin_dir = self.tmp_path / "origin"
        origin_dir.mkdir()
        run_git(["init", "-b", "main"], origin_dir)
        run_git(["config", "user.name", "Codex Test"], origin_dir)
        run_git(["config", "user.email", "codex@example.com"], origin_dir)
        tracked_file = origin_dir / "run_mriqc.sh"
        tracked_file.write_text("#!/bin/bash\necho v1\n")
        run_git(["add", "."], origin_dir)
        run_git(["commit", "-m", "initial"], origin_dir)

        scripts_dir = self.tmp_path / "home" / "lobi-mri-scripts"

        with patch.object(lobi_scripts_module, "GITHUB_REPO_URL", str(origin_dir)):
            with patch.object(lobi_scripts_module, "SCRIPTS_DIR", scripts_dir):
                install_result = self.runner.invoke(lobi_scripts_module.lobi_scripts, ["install"])
                self.assertEqual(install_result.exit_code, 0)

                cloned_file = scripts_dir / "run_mriqc.sh"
                cloned_file.write_text("#!/bin/bash\necho local-change\n")

                tracked_file.write_text("#!/bin/bash\necho v2\n")
                run_git(["add", "run_mriqc.sh"], origin_dir)
                run_git(["commit", "-m", "update"], origin_dir)

                result = self.runner.invoke(lobi_scripts_module.lobi_scripts, ["update"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Repository updated", result.output)
        self.assertEqual((scripts_dir / "run_mriqc.sh").read_text(), "#!/bin/bash\necho v2\n")


if __name__ == "__main__":
    unittest.main()
