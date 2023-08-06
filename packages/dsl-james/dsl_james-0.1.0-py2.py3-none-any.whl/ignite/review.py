"""
Code inspection / review

TODO: include type checking using mypy
"""
from pathlib import Path
import ast
from typing import Union, Dict, List, Optional
from collections import Counter
import re

from loguru import logger

from james.utils import cmd


class CodeInspection:

    FILENAME: str = 'codereview.log'
    EXCLUDE_PATTERN: str = '.git,.eggs,__pycache__,.tox,docs,test,tests,.pytest_cache'

    def __init__(self, path: Union[Path, str]) -> None:
        logger.info(f'Starting code inspection for directory {path}')
        self.path: Path = Path(path)
        self.counts: Dict = {}
        self.totals = {
            'classes': 0,
            'methods': 0,
            'functions': 0,
            'expressions': 0,
        }
        self.error_counts = Counter()

    def count(self) -> None:
        self.counts = CodeCounter(self.path, exclude_pattern=self.EXCLUDE_PATTERN.split(','))()
        for key in self.totals.keys():
            self.totals[key] = sum([x[key] for x in self.counts.values()])

    def lint(self) -> None:
        output_file = (self.path / self.FILENAME).as_posix()

        # run code inspection with flake8
        # N.B. the --output-file option appends instead of replaces, so fix this manmually
        cmd(f'rm {output_file}')
        cmd(f'flake8 \
            --exit-zero \
            --exclude={self.EXCLUDE_PATTERN} \
            --max-line-length=120 \
            --docstring-convention=google \
            --output-file={output_file} \
            .')

        # read the output file
        with open(output_file, 'r') as f:
            result = f.read()
        for line in result.split('\n'):
            try:
                filename, linenumber, char, msg = line.split(':')
                # filter out specifics in message (they are between '' or ())
                msg = re.sub(r'\'[^\']*\'', '<expr>', msg)
                msg = re.sub(r'\([^\)]*\)', '<expr>', msg)
                self.error_counts.update([msg])
            except ValueError:
                logger.debug(f'Cannot parse line "{line}"')

    def __call__(self) -> str:
        self.count()
        self.lint()

        output_file = (self.path / self.FILENAME).as_posix()
        total_issues = sum(self.error_counts.values())
        total_functions = sum(self.totals.values())
        total_score = total_issues / max(total_functions, 1)

        lines = [
            '='*79,
            f'Code Inspection of directory "{self.path}"',
            '='*79,
            '',
            'Code analyzed:'
        ] + [
            f'* {count:3d} {key}'
            for key, count in self.totals.items()
        ] + [
            '',
            f'{total_issues} Issues found:'
        ] + [
            f'{count:3d} {("cases" if count > 1 else "case")} of {msg}'
            for msg, count in self.error_counts.most_common()
        ] + [
            '',
            f'For detailed error messages, see {output_file}'
            'Your total IPE score (issues per element, lower is better) is:',
            f'[ {total_score:.1f} ]',
            '',
            f'For full report, see {output_file}'
        ]
        return '\n'.join(lines)


class CodeCounter:

    def __init__(self, path: Union[Path, str], exclude_pattern: Optional[List[str]] = None) -> None:
        self.path: Path = Path(path)
        self.counts: Dict[str, Dict[str, int]] = {}
        self.exclude_pattern: List[str] = exclude_pattern

    def _should_exclude(self, filename: Path) -> bool:
        for part in filename.parts:
            if part in self.exclude_pattern:
                return True
        return False

    def __call__(self) -> Dict[str, Dict[str, int]]:
        for filename in self.path.rglob('*.py'):
            if self._should_exclude(filename):
                continue
            filename_str = filename.as_posix()
            self.counts[filename_str] = self.count(filename_str)
        return self.counts

    @staticmethod
    def count(filename: str) -> Dict[str, int]:
        with open(filename, 'r') as f:
            # parse the AST of the file
            logger.info(f'parsing {filename}')
            tree = ast.parse(f.read())

        classes = [e for e in tree.body if isinstance(e, ast.ClassDef)]
        methods = [f for c in classes for f in c.body if isinstance(f, ast.FunctionDef)]
        funcs = [f for f in tree.body if isinstance(f, ast.FunctionDef)]
        expressions = [f for f in tree.body if isinstance(f, ast.Expr)]

        return {
            'classes': len(classes),
            'methods': len(methods),
            'functions': len(funcs),
            'expressions': len(expressions)
        }
