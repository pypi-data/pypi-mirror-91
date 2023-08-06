"""
Generalized setup interfaces for cloud platforms


- Azure DevOps
    - Organization
        - list
        - create
    - Project
        - list
        - create
    - Repo
        - list
        - create

- Azure
    - Subscription
        - list
    - Resource group
        - list
        - create

"""
from abc import ABC, abstractmethod
from typing import List, Dict

from loguru import logger

from james.utils import cmd, az_cmd


class PlatformSetup(ABC):

    @abstractmethod
    def get_settings(self) -> List[Dict]:
        pass


class AzureDevOpsSetup(PlatformSetup):

    SETTINGS = ['organization', 'project']

    def __init__(self):
        self._check_requirements()
        self._organization = None
        self._project = None

    @staticmethod
    def _check_requirements():
        # check azure cli
        try:
            az_version = cmd('az --version')
            logger.info(f'Found az cli version {az_version}')
        except SystemError as e:
            logger.error(
                'Azure CLI is not installed. Please install this first from '
                'https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest'
            )
            raise e

        # check azure-devops extension
        try:
            azdevops_version = cmd('az extension show --name "azure-devops" --query version -o tsv')
            logger.info(f'Found azure-devops extension version: {azdevops_version}')
        except SystemError as e:
            logger.error(
                "azure-cli devops extension is missing. Please install it using:"
                "az extension add --name azure-devops"
            )
            raise e

    def get_settings(self):
        return [
            {
                'name': 'organization',
                'type': str,
                'default': 'data-science-lab'
            }, {
                'name': 'project',
                'type': str,
                'default': 'Intern'
            }
        ]

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, value):
        cmd(f'az devops configure --defaults organization=https://dev.azure.com/{self._organization}')
        self._organization = value

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        cmd(f'az devops configure --defaults organization=https://dev.azure.com/{self._organization} project="{value}"')
        self._project = value


class AzureDevOpsResource:

    DEFAULT_ORG = 'data-science-lab'
    SUPPORTED_RESOURCES = ['project']

    def __init__(self, resource_name: str):
        if resource_name not in self.SUPPORTED_RESOURCES:
            raise ValueError(f'Resource type "{resource_name}" is not supported')
        self.resource_name = resource_name

    def list(self) -> List[str]:
        az_cmd(f'devops {self.resource_name} list', {
            'organization': self.DEFAULT_ORG,
            'query': 'value[].name',
            'output': 'tsv'
        })

    def create(self, value: str) -> None:
        az_cmd(f'devops {self.resource_name} create', {
            'name': value,
            'organization': self.DEFAULT_ORG
        })
        self.set(value)

    def set(self, value):
        cmd(f'az devops configure --defaults organization=https://dev.azure.com/{self.DEFAULT_ORG} project={value}')


class AzureResource:

    SUPPORTED_RESOURCES = ['subscription']

    def __init__(self, resource_name: str):
        if resource_name not in self.SUPPORTED_RESOURCES:
            raise ValueError(f'Resource type "{resource_name}" is not supported')
        self.resource_name = resource_name

    def list(self) -> List[str]:
        az_cmd(f'{self.resource_name} list', {
            'query': 'value[].name',
            'output': 'tsv'
        })

    def create(self, value: str) -> None:
        if self.resource_name == 'subscription':
            raise ValueError('Cannot create Azure DevOps organization via CLI. Use the web interface instead.')

        az_cmd(f'{self.resource_name} create', {
            'name': value,
            'detect': 'true'
        })
        self.set(value)

    def set(self, value):
        cmd(f'az {self.resource_name} --set ')
