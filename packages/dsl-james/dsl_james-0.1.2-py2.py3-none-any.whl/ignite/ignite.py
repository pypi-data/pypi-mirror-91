"""Main module."""
from typing import List, Dict, Callable
from collections import OrderedDict

from loguru import logger
from pathlib import Path
from cookiecutter.main import cookiecutter

from james.utils import cmd, az_cmd
from james.config import IgniteConfig


class Ignition:
    """
    Main handler for the actions that need to be executed
    """
    # TODO: possibility to use various cookiecutter temnplates
    COOKIECUTTERS = [
        {
            'name': 'Data science project',
            'url': 'git@ssh.dev.azure.com:v3/data-science-lab/Intern/cookiecutter-data-science'
        }, {
            'name': 'Python package',
            'url': 'git@ssh.dev.azure.com:v3/data-science-lab/Intern/cookiecutter-pypackage',
        }
    ]

    def __init__(self, config: IgniteConfig):
        self.config = config
        self.project_dir = None
        self.stages = OrderedDict({
            'create_repo': {'description': 'Create git repository', 'completed': False},
            'cookiecutter': {'description': 'Download cookiecutter template', 'completed': False},
            'local_repo': {'description': 'Setup local git repository', 'completed': False},
            'python_environment': {'description': 'Create python_environment', 'completed': False},
        })
        self.validate_config()
        self.check_stages()

    def validate_config(self):
        """
        Check if the configuration is ready to go (if init has been run successfully)
        """
        if not self.config.validate():
            raise ValueError('Cannot james. Run ingite init first to set all required variables.')

    def check_stages(self) -> None:
        assert self.get('PROJECT', 'project_name') is not None
        assert self.get('PROJECT', 'repository_name') is not None
        assert self.get('AZUREDEVOPS', 'devops_project') is not None
        for stage_key, stage_info in self.stages.items():
            self.stages[stage_key]['completed'] = self._check_stage(stage_key)

    def _check_stage(self, stage: str) -> bool:
        assert stage in self.stages.keys()

        project_dir = Path.cwd() / self.get('PROJECT', 'project_name')
        if stage == 'create_repo':
            return az_cmd(
                command='repos show',
                params={
                    'organization': f"https://dev.azure.com/{self.get('AZUREDEVOPS', 'devops_organization')}",
                    'project': self.get('AZUREDEVOPS', 'devops_project'),
                    'repository': self.get('PROJECT', 'repository_name')
                },
                return_success=True
            )
        elif stage == 'cookiecutter':
            return project_dir.exists()
        elif stage == 'local_repo':
            return cmd(f'git -C {project_dir} status', return_success=True)
        elif stage == 'python_environment':
            tool = self.get('PROJECT', 'python_environment')
            env_name = self.get('PROJECT', 'project_name')
            if tool == 'no':
                return True
            elif tool == 'conda':
                envs_text = cmd('conda env list')
                envs = map(lambda x: x.split()[0], envs_text.split('\n')[2:])
                return env_name in envs
            elif tool == 'venv':
                return Path(project_dir / 'venv').exists()
            elif tool == 'virtualenv':
                return Path(project_dir / 'venv').exists()
            else:
                return False

    def get(self, section: str, key: str) -> str:
        return self.config.get(section, key)

    def set(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)

    def _create_repo(self) -> None:
        """
        Create repository in Azure DevOps Repos
        """
        assert self.get('PROJECT', 'repository_name') is not None
        #az_cmd('login')
        if self._check_stage('create_repo'):
            logger.warning(f"Repository {self.get('PROJECT', 'repository_name')} already exists. Skipping creation.")
            return
        url = az_cmd('repos create', {
            'organization': f"https://dev.azure.com/{self.get('AZUREDEVOPS', 'devops_organization')}",
            'project': self.get('AZUREDEVOPS', 'devops_project'),
            'name': self.get('PROJECT', 'repository_name'),
            'query': 'sshUrl',
            'output': 'tsv'
        })
        assert url == self.get('PROJECT', 'repository_url'), \
            f"Expected {self.get('PROJECT', 'repository_url')}, but instead found {url}"

        self.stages['create_repo']['completed'] = True

    def _cookiecutter(self) -> None:
        project_dir = Path(self.get('META', 'projects_dir')) / self.get('PROJECT', 'project_name')
        if project_dir.exists():
            logger.warning(f'Directory {project_dir} already exists. Skipping cookiecutter.')
            self.project_dir = project_dir
            return

        logger.info("Starting cookiecutter")
        mandatory = [
            'repository_url',
            'project_name',
            'description',
            'code_dir',
            'author_email',
            'author_name',
        ]
        options = {
            key: self.get('PROJECT', key)
            for key in mandatory
        }
        cookiecutter(
            'git@ssh.dev.azure.com:v3/data-science-lab/Intern/cookiecutter-data-science',
            no_input=True,
            extra_context=options
        )
        self.project_dir = project_dir
        self.stages['cookiecutter']['completed'] = True

    def _local_repository(self):
        assert self.project_dir is not None
        if self._check_stage('local_repo'):
            logger.warning('Git  repository already detected. Not creating a new one')
            return
        logger.info('Creating local git repository')
        dir_spec = f'-C {self.project_dir}'
        cmd(f'git {dir_spec} init')
        cmd(f'git {dir_spec} remote add origin {self.get("PROJECT", "repository_url")}')
        cmd(f'git {dir_spec} add .')
        cmd(f'git {dir_spec} commit -m "Cookiecutter template"')
        logger.info('Push to origin (master)')
        cmd(f'git {dir_spec} push -u origin master')
        logger.info('Creating develop branch')
        cmd(f'git {dir_spec} checkout -b develop')
        cmd(f'git {dir_spec} push origin develop')
        logger.info('Set develop as default branch')
        az_cmd('repos update', {
            'organization': f"https://dev.azure.com/{self.get('AZUREDEVOPS', 'devops_organization')}",
            'project': self.get('AZUREDEVOPS', 'devops_project'),
            'repository': self.get('PROJECT', 'repository_name'),
            'default-branch': 'develop'
        })
        self.stages['local_repo']['completed'] = True

    def _go_to_project(self):
        # enter project dir
        # dirname = self.get('PROJECT', 'project_name')
        # cmd(f'cd {dirname}')

        # copy config file to project dir!
        self.config.consolidate()

    def _create_environment(self) -> None:
        if self._check_stage('python_environment'):
            logger.warning('Python environment already exists. Skipping creation.')
            return
        logger.info('Creating Python environment')
        tool = self.get('PROJECT', 'python_environment')
        env_name = self.get('PROJECT', 'project_name')
        version = self.get('PROJECT', 'python_version')
        if tool == 'conda':
            #cmd(f'conda create -n {env_name} python={version} --yes && conda activate {env_name}')
            # activating doesn't work
            cmd(f'conda create -n {env_name} python={version} --yes')
        elif tool == 'venv':
            cmd('python3 -m venv venv')
            try:
                # Mac / Linux
                cmd('source ./venv/bin/activate')
            except SystemError:
                # Windows
                cmd('./venv/Scripts/activate')
        elif tool == 'virtualenv':
            cmd('virtualenv -p venv')
            try:
                # Mac / Linux
                cmd('source ./venv/bin/activate')
            except SystemError:
                # Windows
                cmd('./venv/Scripts/activate')

        self.stages['python_environment']['completed'] = True

    def stage_report(self) -> str:
        lines = ['james execution status:']
        for _, stage in self.stages.items():
            done = '[✔]' if stage['completed'] else '[ ]'
            lines.append(f'{done} {stage["description"]}')
        return '\n'.join(lines)

    def execute(self, callback_fn: Callable) -> None:
        # checks
        project_name = self.get('PROJECT', 'project_name')
        assert project_name is not None

        callback_fn('Starting james execution')
        callback_fn(self.stage_report())
        self._create_repo()
        callback_fn(self.stage_report())
        self._cookiecutter()
        callback_fn(self.stage_report())
        self._local_repository()
        callback_fn(self.stage_report())
        self._go_to_project()
        callback_fn(self.stage_report())
        self._create_environment()
        callback_fn(self.stage_report())
        callback_fn('Done!')
