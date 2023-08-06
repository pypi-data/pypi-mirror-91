"""
Setup for Azure settings
"""
import json
from typing import List, Dict

from loguru import logger

from james.utils import cmd, az_cmd


class AzureSetup:

    DEFAULT_ORG = 'data-science-lab'
    DEFAULT_PROJECT = 'Intern'

    def __init__(self) -> None:
        self.projects = None
        self.subscriptions = None
        self._check_requirements()
        #self._login()

        # set default organization & project
        cmd(f'az devops configure --defaults organization=https://dev.azure.com/{self.DEFAULT_ORG} project={self.DEFAULT_PROJECT}')

    @staticmethod
    def _check_requirements() -> None:
        """
        Check if required tools are installed

        Raises:
            SystemError if not installed
        """
        # check az cli
        try:
            az_version = cmd('az --version', return_success=True)
            logger.info(f'✔ az cli installed')
        except SystemError as e:
            logger.error(
                'Azure CLI is not installed. Please install this first from '
                'https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest'
            )
            raise e

        # check azure-devops extension
        try:
            azdevops_version = cmd('az extension show --name "azure-devops" --query version -o tsv', return_success=True)
            logger.info(f'✔ az cli azure-devops extension installed (version {azdevops_version})')
        except SystemError as e:
            logger.error(
                "azure-cli devops extension is missing. Please install it using:"
                "az extension add --name azure-devops"
            )
            raise e

    @staticmethod
    def _login() -> None:
        cmd('az login')

    def get_subscriptions(self, no_cache: bool = False) -> List[Dict]:
        """

        Returns:
            str: printable table containing info on all subscriptions

        Raises:
            SystemError: if command fails
        """
        if self.subscriptions is None or no_cache:
            json_str = cmd('az account list')
            self.subscriptions = json.loads(json_str)
        return self.subscriptions

    @staticmethod
    def set_subscription(subscription_id: str) -> None:
        cmd(f'az account set --subscription {subscription_id}')

    def get_devops_projects(self, no_cache: bool = False) -> List[str]:
        if self.projects is None or no_cache:
            projects_str = cmd('az devops project list --query value[].name -o tsv')
            self.projects = projects_str.split('\n')
        return self.projects

    @classmethod
    def set_devops_project(cls, project: str) -> None:
        cmd(f'az devops configure --defaults organization=https://dev.azure.com/{cls.DEFAULT_ORG} project="{project}"')


