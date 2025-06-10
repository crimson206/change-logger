#!/usr/bin/env python3

import subprocess
import shutil
from pathlib import Path
from typing import Optional, List


def run_changelog(
    template_file: str | Path,
    templates_dir: str = "templates",
    semantic_release_args: Optional[List[str]] = None,
) -> bool:

    template_file = Path(template_file)
    templates_dir = Path(templates_dir)
    target_template = templates_dir / "changelog.md.j2"

    if semantic_release_args is None:
        semantic_release_args = ["changelog"]

    # Check template exists
    if not template_file.exists():
        print(f"❌ Template not found: {template_file}")
        return False

    # Create templates dir
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Copy template
    shutil.copy2(template_file, target_template)
    print(f"📋 Copied: {template_file} → {target_template}")

    # Run semantic-release
    try:
        result = subprocess.run(
            ["semantic-release"] + semantic_release_args,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ semantic-release completed successfully")
            if result.stdout:
                print("STDOUT:", result.stdout)
            return True
        else:
            print("❌ semantic-release failed")
            print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ semantic-release timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


success = run_changelog("templates/released_changelog.md.j2")
if success:
    print("🎉 Done! Check CHANGELOG.md")
else:
    print("💥 Failed")
