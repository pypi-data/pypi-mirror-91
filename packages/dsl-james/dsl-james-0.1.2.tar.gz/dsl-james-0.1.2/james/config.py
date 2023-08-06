from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path
from typing import Callable, Tuple, Dict, List, Union
import re

import click
from loguru import logger

from james.utils import cmd, ProjectNameType, PythonVersionType


class IgniteUnknownSettingError(Exception):
    pass


class IgniteMissingSetupError(Exception):
    pass


class IgniteInvalidStateError(Exception):
    pass


class IgniteConfig(ConfigParser):

    FILE_STUB = '.james'
    PROJECT_DIR = Path.cwd()
    BASE_DIR = Path.home()
    META_SECTION_NAME = 'META'
    PROJECTS_DIR_FIELD = 'projects_dir'

    def __init__(self, extension: str = '.ini', test_mode: bool = False) -> None:
        super().__init__()

        if extension not in ['.ini', '.json']:
            raise ValueError(f'Unsupported extenstion {extension}. Use .ini or .json')
        self.extension = extension
        self.test_mode = test_mode
        self.projects_dir = self.get_projects_dir()
        self.is_existing_project = False
        self.callbacks = {}

        # softly set default values
        for section, var in self.iter_settings():
            # calling our own set method would write the default values to file, before we read the file
            # effectively overwriting them with defaults; the parent's set does not
            self.set(section, var['name'], var['default'](), persist=False)

        # look for file with settings
        file_here = Path.cwd() / f'{self.FILE_STUB}{extension}'
        file_base = self.BASE_DIR / f'{self.FILE_STUB}{extension}'

        if file_here.exists():
            if file_here != file_base and self.projects_dir is None:
                raise IgniteMissingSetupError('Could not read projects_dir setting from home dir config file. '
                                              'Make sure to run james setup first')

            if not file_here.as_posix().startswith(self.projects_dir):
                raise ValueError(f'Existing config file "{file_here}" found, but it is not inside projects dir "{self.projects_dir}"')
            # use an existing config file for a project
            self.filename = file_here
            self.read(self.filename)
            self.is_existing_project = True  # indicate that this config is project-specific
            logger.info(f'Reading config from {self.filename}')
        elif file_base.exists():
            # use the default config file in the user home dir
            self.filename = file_base
            self.read(self.filename)
            logger.info(f'Reading config from {self.filename}')
        else:
            self.filename = file_base
            logger.info('No existing config file found')

        self._set_callbacks()

        # remove any deprecated variables
        self.cleanup()

    def get_projects_dir(self) -> Union[str, None]:
        """
        Try to identiy the projects_dir (in the META section) from the base config file

        Returns:
            str: path if found else None
        """
        try:
            parser = ConfigParser()
            parser.read(self.BASE_DIR / f'{self.FILE_STUB}{self.extension}')
            return parser.get(self.META_SECTION_NAME, self.PROJECTS_DIR_FIELD)
        except Exception:
            return None

    def _set_callbacks(self) -> None:
        # get settings
        settings, derived_settings = self.get_settings()

        # set callbacks for derived settings
        self.callbacks = {}
        for section, settings_list in derived_settings.items():
            for item in settings_list:
                for var_section, var in self.iter_settings(project_only=False):
                    if var['name'] in item['value']:
                        logger.debug(f'Adding callback for variable {item["name"]} depending on {var["name"]}')
                        self._add_callback(
                            section=section,
                            name=var["name"],
                            fn=self._create_callback_fn(
                                section=section,
                                name=item['name'],
                                value=item['value']
                            )
                        )

                for item2 in settings_list:
                    if item2['name'] in item['value']:
                        logger.debug(f'Adding callback for variable {item["name"]} depending on {item2["name"]}')
                        self._add_callback(
                            section=section,
                            name=item2["name"],
                            fn=self._create_callback_fn(
                                section=section,
                                name=item['name'],
                                value=item['value']
                            )
                        )

    def _render_template(self, template: str) -> str:
        """
        From a template in the form of 'https://gitserver.com/{PROJECT.project_name|.replace("-", "_")}'
        Parse the config var and apply the transformation

        Args:
            template (str): string with reference to config variable enclosed in {}

        Returns:
            str: value derived from existing value
        """
        def _replacement_func(matched_obj):
            expr = matched_obj.group(1)
            if '|' in expr:
                var, op = expr.split('|')
            else:
                var, op = expr, ''
            logger.debug(var)
            var_value = self.get(*var.split('.'))
            return eval(f'"{var_value}"{op}')

        return re.sub(r'\{([^}]+)\}', _replacement_func, template)

    def _create_callback_fn(self, section, name, value) -> Callable:
        """
        Create an update callback

        Args:
            section: sectrion name
            name: variable name
            value (str): a template referencing an existing value

        Returns:
            Callable: callback function
        """
        def tmp_fn():
            self.set(section, name, self._render_template(value))

        return tmp_fn

    def _add_callback(self, section: str, name: str, fn: Callable) -> None:
        """
        Registers a new callback to trigger when given variable changes

        Args:
            section:
            name:
            fn:

        Returns:

        """
        key = f'{section}.{name}'
        if key not in self.callbacks:
            self.callbacks[key] = []
        self.callbacks[key].append(fn)

    def clear(self) -> None:
        """
        Remove all settings (except META)
        """
        for section in self.sections():
            if section == 'META':
                continue
            self.remove_section(section)

    def __iter__(self) -> List[Tuple[str, str, str]]:
        return [
            (section, key, value)
            for section in self.sections()
            for key, value in self.items(section)
        ]

    def get_current_settings(self, as_dict: bool = True) -> Union[Dict, List[Tuple[str, str, str]]]:
        if as_dict:
            return {
                section: dict(self.items(section))
                for section in self.sections()
            }
        else:
            return [
                (section, key, value)
                for section in self.sections()
                for key, value in self.items(section)
            ]

    @staticmethod
    def get_settings() -> Tuple[Dict, Dict]:
        settings = {
            'PROJECT': [
                {
                    'name': 'project_name',
                    'description': 'Name of the project (use lowercase-with-dashes)',
                    'type': ProjectNameType(),
                    'default': lambda: ''
                }, {
                    'name': 'description',
                    'description': 'Short description of the project',
                    'type': str,
                    'default': lambda: ''
                }, {
                    'name': 'python_version',
                    'description': 'Python version to use',
                    'type': PythonVersionType(),
                    'default': lambda: '3.8'
                },
                {
                    'name': 'author_name',
                    'description': 'Your full name (otherwise name of the team)',
                    'type': str,
                    'default': lambda: cmd('git config --get user.name')
                },
                {
                    'name': 'author_email',
                    'description': 'Your email address (otherwise of the team)',
                    'type': str,
                    'default': lambda: cmd('git config --get user.email')
                },
                {
                    'name': 'python_environment',
                    'description': 'Crerate a new Python environment?',
                    'type': click.Choice(['conda', 'venv', 'virtualenv', 'no']),
                    'default': lambda: 'conda' if cmd('conda --version', return_success=True) else 'no'
                },
            ],
            'AZURE': [
                {
                    'name': 'subscription_id',
                    'description': 'Id of the Azure subscription to use',
                    'type': str,
                    'default': lambda: ''
                }, {
                    'name': 'subscription_name',
                    'description': 'Name of the Azure subscription to use',
                    'type': str,
                    'default': lambda: 'Intern'
                }
            ],
            'AZUREDEVOPS': [
                {
                    'name': 'devops_organization',
                    'description': 'Name of the Azure DevOps organization to use',
                    'type': str,
                    'default': lambda: 'data-science-lab'
                }, {
                    'name': 'devops_project',
                    'description': 'Name of the Azure DevOps project to use',
                    'type': str,
                    'default': lambda: 'Intern'
                }
            ]
        }

        derived_settings = {
            'PROJECT': [{
                'name': 'repository_name',
                'value': '{PROJECT.project_name}'
            }, {
                'name': 'repository_url',
                'value': 'git@ssh.dev.azure.com:v3/{AZUREDEVOPS.devops_organization}/{AZUREDEVOPS.devops_project}/{PROJECT.repository_name}'
            }, {
                'name': 'code_dir',
                'value': '{PROJECT.project_name|.replace("-", "_")}'
            }]
        }

        return settings, derived_settings

    def cleanup(self):
        expected = [
            (section, var['name'])
            for section, var in self.iter_settings(include_derived=True)
        ]
        current = [
            (section, key)
            for (section, key, value) in self.get_current_settings(as_dict=False)
            if section != 'META'
        ]
        for section_varname_pair in current:
            if section_varname_pair not in expected:
                section, varname = section_varname_pair
                logger.warning(f'Removing unexpected option {section}.{varname}')
                self.remove_option(section, varname)
                #self._save()

    @classmethod
    def iter_settings(cls, project_only: bool = False, include_derived: bool = False) -> Tuple[str, Dict]:
        settings, derived_settings = cls.get_settings()
        for section, info in settings.items():
            if project_only and section != 'PROJECT':
                continue
            for variable in info:
                yield section, variable

        if include_derived:
            for section, settings_list in derived_settings.items():
                for item in settings_list:
                    if project_only and section != 'PROJECT':
                        continue
                    yield section, item

    def _save(self) -> None:
        if self.test_mode:
            # we don't want to overwrite real files when e.g. running tests
            logger.info('TEST MODE: not saving to file')
            return

        logger.info(f'saving to {self.filename}')
        with open(self.filename, 'w') as f:
            self.write(f)

    def get(self, section: str, key: str, **kwargs) -> str:
        try:
            return super().get(section, key, **kwargs)
        except (NoSectionError, NoOptionError):
            raise IgniteUnknownSettingError(f'Setting {section}.{key} not found')

    def set(self, section: str, key: str, value: str, persist: bool = True, **kwargs) -> None:
        if section not in self.sections():
            logger.info(f'Adding section {section}')
            self.add_section(section)
        super().set(section, key, value, **kwargs)

        # check for callbacks on this variable
        callback_key = f'{section}.{key}'
        if callback_key in self.callbacks:
            for callback_fn in self.callbacks[callback_key]:
                callback_fn()

        # save to file
        if persist:
            self._save()

    def consolidate(self) -> None:
        """
        Copy temporary config file in user dir to project dir
        """
        project_name = self.get('PROJECT', 'project_name')
        new_dir = Path.cwd() / project_name
        if not new_dir.exists():
            raise ValueError(f'Expected directory {new_dir} to exist but it doesn\'t')
        self.filename = new_dir / f'{self.FILE_STUB}{self.extension}'
        self._save()

    def validate(self) -> bool:
        """
        Check if all settings are set

        Returns:
            bool
        """
        for (section, key, value) in self.get_current_settings(as_dict=False):
            if not value:
                return False
        return True

    def show(self, method: Callable = print) -> None:
        #method({section: dict(self[section]) for section in self.sections()})
        method(f'Settings read from {self.filename}:\n')
        method(cmd(f'cat {self.filename.resolve()}'))
