"""Console script for james."""
import sys
from pathlib import Path

from loguru import logger
import click

from james import __version__
from james.utils import cmd, PythonVersionType
from james.config import IgniteConfig, IgniteInvalidStateError
from james.azure import AzureSetup
from james.james import Ignition
from james.review import CodeInspection


logger.remove(0)
logger.add(sys.stderr, level='INFO')


INTRO_TEXT = r"""
   /\      ██████╗ ███████╗██╗         ██╗ ██████╗ ███╗   ██╗██╗████████╗███████╗
  (  )     ██╔══██╗██╔════╝██║         ██║██╔════╝ ████╗  ██║██║╚══██╔══╝██╔════╝
  (  )     ██║  ██║███████╗██║         ██║██║  ███╗██╔██╗ ██║██║   ██║   █████╗  
 /|/\|\    ██║  ██║╚════██║██║         ██║██║   ██║██║╚██╗██║██║   ██║   ██╔══╝  
/_||||_\   ██████╔╝███████║███████╗    ██║╚██████╔╝██║ ╚████║██║   ██║   ███████╗
   **      ╚═════╝ ╚══════╝╚══════╝    ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝
  ********************************************** powered by Data Science Lab ////                                                                                                   

Fast & easy project startup 
"""


"""
- Main: 
- setup: only set variables
- show: show variables / status
- go: execute (if vars are set)

Typical workflow

$ [~/projects/] james setup
    -> reads / creates file in ~
$ [~/projects/] james go
    -> reads file in ~, copies file to ~/projects/my-project/  
$ [~/projects/my-project] james show
    -> reads file in ~/projects/my-project/ 
"""


@click.group()
@click.version_option(message='You are using %(prog)s version %(version)s')
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    Console script for james.
    The main function only reads the config
    """
    click.echo(INTRO_TEXT)

    logger.info('Creating config object')
    ctx.obj = IgniteConfig()


@main.command()
@click.pass_context
def setup(ctx: click.Context) -> None:
    """
    One-time setup for generic settings like
    - Azure & Azure DevOps defaults
    - Projects dir

    Args:
        ctx (click.Context): ctx.obj contains the IgniteConfig object
    """
    # handle git provider
    git_provider = click.prompt(
        text='Choose a git provider',
        type=click.Choice(['Azure DevOps Repos', 'Github'], case_sensitive=True),
        default='Azure DevOps Repos'
    )
    ctx.obj.set('META', 'git_provider', git_provider)
    if git_provider == 'Azure DevOps Repos':
        devops_organization = click.prompt(
            text='Enter Azure DevOps organization name (https://dev.azure.com/<organization>)',
            type=str,
            default='data-science-lab'
        )
        ctx.obj.set('AZUREDEVOPS', 'devops_organization', devops_organization)
    elif git_provider == 'Github':
        github_username = click.prompt(
            text='Enter Github username',
            type=str,
            default=''
        )
        ctx.obj.set('GITHUB', 'github_username', github_username)
    else:
        raise ValueError(f'Unsupported git provider "{git_provider}"')

    # handle cloud resource provider
    cloud_provider = click.prompt(
        text='Choose a cloud provider (currently only Azure is supported!)',
        type=click.Choice(['Azure'], case_sensitive=True),
        default='Azure'
    )
    ctx.obj.set('META', 'cloud_provider', cloud_provider)
    if cloud_provider == 'Azure':
        # ask subscription
        pass

    # set user project directory
    projects_dir = click.prompt(
        text='Choose a directory containing your projects (use "~" for your home dir)',
        type=click.Path(),
        default='~/projects'
    )
    projects_dir = Path(projects_dir.replace('~', Path.home().as_posix())).resolve()
    if not projects_dir.exists():
        raise FileExistsError(f'Directory {projects_dir} does not exist. Please check if it\'s correct.')
    ctx.obj.set('META', 'projects_dir', projects_dir.as_posix())


@main.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """
    Set all settings via prompts

    Args:
        ctx (click.Context): ctx.obj contains the IgniteConfig object
    """
    if ctx.obj.is_existing_project:
        raise IgniteInvalidStateError(f'Current config defines an existing project. Cannot call james init here.')

    # new project: clear existing values in config file
    ctx.obj.clear()

    if ctx.obj.get('META', 'cloud_provider') == 'Azure':
        # set Azure config
        azsetup = AzureSetup()

        # azure subscription
        subscriptions = azsetup.get_subscriptions()
        options = [
            sub['name']
            for sub in subscriptions
            if sub['isDefault']
        ] + [
            sub['name']
            for sub in subscriptions
            if not sub['isDefault']
        ]
        subscription_name = click.prompt(
            text='Choose Azure subscription',
            type=click.Choice(options, case_sensitive=True),
            default=options[0]
        )
        subscription_id = [
            sub['id']
            for sub in subscriptions
            if sub['name'] == subscription_name
        ][0]
        ctx.obj.set('AZURE', 'subscription_name', subscription_name)
        ctx.obj.set('AZURE', 'subscription_id', subscription_id)
        azsetup.set_subscription(subscription_id)

    if ctx.obj.get('META', 'git_provider') == 'Azure DevOps Repos':
        # Azure DevOps settings
        devops_projects = azsetup.get_devops_projects()
        project = click.prompt(
            text='Choose Azure DevOps project',
            type=click.Choice(devops_projects, case_sensitive=True),
            default=azsetup.DEFAULT_PROJECT
        )
        ctx.obj.set('AZUREDEVOPS', 'devops_organization', azsetup.DEFAULT_ORG)
        ctx.obj.set('AZUREDEVOPS', 'devops_project', project)
        azsetup.set_devops_project(project)

    # prompt for project setting values
    for section, var in ctx.obj.iter_settings(project_only=True):
        value = click.prompt(
            text=var['description'],
            type=var['type'],
            default=var['default']()
        )
        ctx.obj.set(section, var['name'], value)

    ctx.obj.cleanup()


@main.command()
@click.pass_context
@click.argument('section')
@click.argument('key')
@click.argument('value')
def set(ctx: click.Context, section: str, key: str, value: str) -> None:
    """
    Set a single value
    """
    logger.info(f'Setting {section}.{key} = {value}')
    ctx.obj.set(section, key, value)


@main.command()
@click.pass_context
def show(ctx: click.Context) -> None:
    """
    Display settings
    """
    ctx.obj.show(method=click.echo)


@main.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """
    Check status of stages for ignition
    """
    plan = Ignition(config=ctx.obj)
    click.echo(plan.stage_report())


@main.command()
@click.pass_context
def review(ctx: click.Context) -> None:
    """
    Linting / code review
    """
    #if ctx.obj.filename.parent
    report = CodeInspection(Path.cwd())()
    click.echo(report)


@main.command()
@click.pass_context
@click.confirmation_option(prompt="""
This will execute the actual project setup work:
- create a git repository
- create a new local project dir from a cookiecutter template
- create a python environment

Are you sure you want to continue?
""")
def go(ctx: click.Context) -> None:
    """
    Execute actions for project start
    """
    Ignition(config=ctx.obj).execute(callback_fn=click.echo)


if __name__ == "__main__":
    main()
