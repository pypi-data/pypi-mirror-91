# james - at your service

CLI tool for starting up a new project

Before:
- Go to Azure DevOps
  - select project
  - go to Repos
  - create new repo
  - copy clone url
- Run cookiecutter
  - get cookiecutter url and start
  - paste clone url
  - fill in stuff
- Setup local repo
  - git remote set-url
  - git add template files
  - git commit & push
  - git create dev branch
- Create python env

After:
- james init
  - fill in stuff
- james go

What it does is:
- prompt for settings
- create a new git repository
- apply cookiecutter template
- setup a local git repo and link it to the remote
- create python environment


## Usage

### One time setup:
- `pip install dsl-james`  (can be in your base Python environment)
- `james setup` for some general settings

### Starting a new project:
- `james init` will define a new project and prompt your for configuration settings
- `james show` will show configuration (optional)
  - when inside a project dir, it will show configuration of that specific project
  - when inside any other dir, it will show the default configuration
- `james status` will show the status of ignition phases (optional)
- `james go` to execute
- `james review` for code inspection

## Info

james will create `.james.ini` config files:
- One in your home dir (~). This will contain base info (from the `setup`), as well as project-specific info from the last project you defined with `init`.
- One for each project, located in `<projects-dir>/<your-project>`. This is basically a copy of the generic file.
When calling amy james command, james will use the project's config file

## To Do
- [x] Azure setup
- [x] Azure DevOps setup
- [x] Project setup
- [x] Create git repository
- [x] Cookiecutter
- [ ] Support for multiple cookiecutter templates




## Credits
This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.

- Cookiecutter: <https://github.com/audreyr/cookiecutter>
- `audreyr/cookiecutter-pypackage`: <https://github.com/audreyr/cookiecutter-pypackage>
