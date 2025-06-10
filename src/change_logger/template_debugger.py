#!/usr/bin/env python3
"""
Template Debugger for semantic-release changelog templates
Tests individual jinja2 syntaxes to identify working and failing patterns
"""

import subprocess
import os
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any
import json
from dataclasses import dataclass


@dataclass
class TestResult:
    syntax: str
    success: bool
    error_message: str = ""
    changelog_content: str = ""
    stdout: str = ""
    stderr: str = ""


class TemplateDebugger:
    def __init__(self, template_path: str = "templates/changelog.md.j2"):
        self.template_path = Path(template_path)
        self.base_template = self._get_base_template()
        self.passed_syntaxes: List[str] = []
        self.failed_syntaxes: List[TestResult] = []
        self.test_results: List[TestResult] = []
        
    def _get_base_template(self) -> str:
        """Get minimal working base template"""
        return """# Changelog

All notable changes to this project will be documented in this file.

{SYNTAX_PLACEHOLDER}
"""

    def _create_test_template(self, syntax: str) -> str:
        """Create a test template with the given syntax"""
        return self.base_template.replace("{SYNTAX_PLACEHOLDER}", syntax)
    
    def _backup_original_template(self) -> Path:
        """Backup the original template if it exists"""
        if self.template_path.exists():
            backup_path = self.template_path.with_suffix('.j2.backup')
            shutil.copy2(self.template_path, backup_path)
            return backup_path
        return None
    
    def _restore_template(self, backup_path: Path):
        """Restore the original template"""
        if backup_path and backup_path.exists():
            shutil.copy2(backup_path, self.template_path)
            backup_path.unlink()
    
    def test_syntax(self, syntax: str) -> TestResult:
        """Test a single syntax by running semantic-release changelog"""
        print(f"Testing: {syntax[:50]}...")
        
        # Create template directory if it doesn't exist
        self.template_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup original template
        backup_path = self._backup_original_template()
        
        try:
            # Write test template
            test_template = self._create_test_template(syntax)
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write(test_template)
            
            # Run semantic-release changelog
            result = subprocess.run(
                ['semantic-release', 'changelog'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Read generated changelog if it exists
            changelog_content = ""
            changelog_path = Path("CHANGELOG.md")
            if changelog_path.exists():
                with open(changelog_path, 'r', encoding='utf-8') as f:
                    changelog_content = f.read()
            
            # Determine success
            success = result.returncode == 0 and "error" not in result.stderr.lower()
            
            test_result = TestResult(
                syntax=syntax,
                success=success,
                error_message=result.stderr if not success else "",
                changelog_content=changelog_content,
                stdout=result.stdout,
                stderr=result.stderr
            )
            
            if success:
                self.passed_syntaxes.append(syntax)
                print(f"  ✅ PASSED")
            else:
                self.failed_syntaxes.append(test_result)
                print(f"  ❌ FAILED: {result.stderr[:100]}...")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            test_result = TestResult(
                syntax=syntax,
                success=False,
                error_message="Timeout after 30 seconds"
            )
            self.failed_syntaxes.append(test_result)
            print(f"  ⏰ TIMEOUT")
            return test_result
            
        except Exception as e:
            test_result = TestResult(
                syntax=syntax,
                success=False,
                error_message=str(e)
            )
            self.failed_syntaxes.append(test_result)
            print(f"  💥 EXCEPTION: {str(e)}")
            return test_result
            
        finally:
            # Restore original template
            self._restore_template(backup_path)
    
    def test_all_syntaxes(self, test_syntaxes: List[str]) -> Dict[str, Any]:
        """Test all syntaxes and return summary"""
        print(f"🚀 Testing {len(test_syntaxes)} syntax patterns...\n")
        
        for i, syntax in enumerate(test_syntaxes, 1):
            print(f"[{i}/{len(test_syntaxes)}] ", end="")
            result = self.test_syntax(syntax)
            self.test_results.append(result)
            print()  # Empty line for readability
        
        return self.get_summary()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of test results"""
        total_tests = len(self.test_results)
        passed_count = len(self.passed_syntaxes)
        failed_count = len(self.failed_syntaxes)
        
        return {
            "total_tests": total_tests,
            "passed": passed_count,
            "failed": failed_count,
            "success_rate": f"{(passed_count/total_tests*100):.1f}%" if total_tests > 0 else "0%",
            "passed_syntaxes": self.passed_syntaxes,
            "failed_syntaxes": [
                {
                    "syntax": result.syntax,
                    "error": result.error_message
                }
                for result in self.failed_syntaxes
            ]
        }
    
    def print_summary(self):
        """Print a nice summary of test results"""
        summary = self.get_summary()
        
        print("=" * 60)
        print("🧪 TEMPLATE DEBUGGING SUMMARY")
        print("=" * 60)
        print(f"Total tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"📊 Success rate: {summary['success_rate']}")
        print()
        
        if summary['passed_syntaxes']:
            print("✅ WORKING SYNTAXES:")
            for syntax in summary['passed_syntaxes']:
                print(f"  • {syntax}")
            print()
        
        if summary['failed_syntaxes']:
            print("❌ FAILED SYNTAXES:")
            for failed in summary['failed_syntaxes']:
                print(f"  • {failed['syntax'][:80]}...")
                print(f"    Error: {failed['error'][:100]}...")
                print()
    
    def save_results(self, output_file: str = "template_debug_results.json"):
        """Save detailed results to JSON file"""
        results = {
            "summary": self.get_summary(),
            "detailed_results": [
                {
                    "syntax": result.syntax,
                    "success": result.success,
                    "error_message": result.error_message,
                    "changelog_content": result.changelog_content,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                for result in self.test_results
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Detailed results saved to: {output_file}")
    
    def generate_working_template(self, output_file: str = "templates/changelog_working.md.j2"):
        """Generate a template with only working syntaxes"""
        if not self.passed_syntaxes:
            print("❌ No working syntaxes found!")
            return
        
        template_content = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

"""
        
        # Add working syntaxes
        for syntax in self.passed_syntaxes:
            template_content += f"\n{syntax}\n"
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"📝 Working template generated: {output_file}")


def main():
    # Test syntaxes to try
    test_syntaxes = [
        # Basic variable access
        "{{ context.repo_name }}",
        "{{ context.repo_owner }}",
        "{{ context.hvcs_type }}",
        
        # Context history access
        "{{ context.history }}",
        "{{ context.history.unreleased }}",
        "{{ context.history.released }}",
        
        # Loops
        "{% for key, value in context.history.unreleased.items() %}{{ key }}{% endfor %}",
        "{% for version, release in context.history.released.items() %}{{ version }}{% endfor %}",
        
        # Conditionals
        "{% if context.history.unreleased %}Has unreleased{% endif %}",
        "{% if context.history.released %}Has releases{% endif %}",
        
        # Filters
        "{{ context.repo_name | title }}",
        "{{ context.history.unreleased.keys() | list }}",
        
        # Complex expressions
        "{% if context.history.unreleased and context.history.unreleased.values() | sum(start=[]) | length > 0 %}Unreleased changes{% endif %}",
        
        # Date formatting
        "{% for version, release in context.history.released.items() %}{{ release.tagged_date.strftime('%Y-%m-%d') }}{% endfor %}",
        
        # GitHub links
        '{{ "https://github.com/" + context.repo_owner + "/" + context.repo_name }}',
        
        # Commit details - basic (기존)
        """{% for commit_type, commits in context.history.unreleased.items() %}
{% for commit in commits %}
- {{ commit.description }}
{% endfor %}
{% endfor %}""",

        # Commit details - enhanced tests
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.descriptions }}{% endfor %}{% endfor %}",
        
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.descriptions[0] if commit.descriptions else 'No description' }}{% endfor %}{% endfor %}",
        
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.descriptions | join(' ') }}{% endfor %}{% endfor %}",
        
        # Check for body/content fields
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.body if commit.body else 'No body' }}{% endfor %}{% endfor %}",
        
        # Check commit attributes
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.__dict__.keys() | list }}{% endfor %}{% endfor %}",
        
        # Try different description access patterns
        """{% for commit_type, commits in context.history.unreleased.items() %}
{% for commit in commits %}
Title: {{ commit.descriptions[0] if commit.descriptions else 'No title' }}
{% if commit.descriptions and commit.descriptions | length > 1 %}
Body: {{ commit.descriptions[1:] | join('\\n') }}
{% endif %}
{% endfor %}
{% endfor %}""",

        # Try breaking_descriptions
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.breaking_descriptions }}{% endfor %}{% endfor %}",
        
        # Full commit info test
        """{% for commit_type, commits in context.history.unreleased.items() %}
### {{ commit_type }}
{% for commit in commits %}
- **{{ commit.descriptions[0] if commit.descriptions else 'No title' }}**
{% if commit.descriptions and commit.descriptions | length > 1 %}
  {% for desc in commit.descriptions[1:] %}
  {{ desc }}
  {% endfor %}
{% endif %}
{% if commit.breaking_descriptions %}
  **BREAKING CHANGES:**
  {% for breaking in commit.breaking_descriptions %}
  - {{ breaking }}
  {% endfor %}
{% endif %}
{% endfor %}
{% endfor %}""",

        # Test commit hash access
        "{% for commit_type, commits in context.history.unreleased.items() %}{% for commit in commits %}{{ commit.commit.hexsha[:8] }}{% endfor %}{% endfor %}",
        
        # Test with GitHub links
        """{% for commit_type, commits in context.history.unreleased.items() %}
{% for commit in commits %}
- {{ commit.descriptions[0] if commit.descriptions else 'No description' }} ([{{ commit.commit.hexsha[:8] }}](https://github.com/{{ context.repo_owner }}/{{ context.repo_name }}/commit/{{ commit.commit.hexsha }}))
{% endfor %}
{% endfor %}""",
    ]
    
    template_path = "templates/changelog.md.j2"
    
    # Initialize debugger
    debugger = TemplateDebugger(template_path)
    
    # Run tests
    debugger.test_all_syntaxes(test_syntaxes)
    
    # Print summary
    debugger.print_summary()
    
    # Save results
    debugger.save_results()
    
    # Generate working template
    debugger.generate_working_template()


if __name__ == "__main__":
    main()