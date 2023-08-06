# repo-tools

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![CircleCI](https://circleci.com/gh/lightspeed-hospitality/repo-tools.svg?style=svg&circle-token=fbdf038d40feb74aec465d01c7aa15b7ee74062a)](https://app.circleci.com/pipelines/github/lightspeed-hospitality/repo-tools)

<p align="center">
  <a href="#development">Development</a> •
  <a href="#architecture--documentation">Documentation</a> •
  <a href="#how-to-contribute">Contribute</a> •
  <a href="#support--feedback">Support</a>
</p>

This is a small Multi Repo CLI that allows you to apply changes to multiple projects at the same time.

---

## Use it!

```console
pip install repo-tools
```

```console
$ rt --help
Usage: rt [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  config   Configure repo_tools
  exec     Execute an arbitrary command
  gh       Interact with github
  snippet  Run snippets (custom snippets can be registered)
```

### Required Setup

* Display your config:
```console
rt config show
```

* Create your Github config:
```console
rt config gh setup
```
_Note_:
To create your config you will need to have a Personal Github Oauth Token, that can be created [here](https://github.com/settings/tokens).
Make sure to give it `repo:all` and `admin:org` permissions.


* Register Projects
```console
rt config projects detect ./<your-projects-dir>
```

* Register Snippets
```console
rt snippet register <path-to-snippet-file> | <path-to-dir-with-snippets>
```

## Development

### Setup

This project uses poetry for dependency management, let's install it:
```console
pip install poetry
```

### Run

You can use poetry to install all dependencies and use the current state of the CLI as follows:
```console
poetry install
poetry shell # opens new shell in virtual env
> rt config show
> ...
```

## How to Contribute

In order to contribute you just have to have Python installed on your machine. In case you do not have it installed get it from [python.org](https://www.python.org/downloads/).

#### Linting Tool

This project is using [pre-commit](https://pre-commit.com/) to enable linting and auto-formatting as a pre-commit hook.
The hooks are configured in [.pre-commit-config.yaml](./.pre-commit-config.yaml).

To install the hooks you have to run the following command (only once):
```bash
pip install pre-commit
pre-commit install
```

Then you can trigger all the hooks manually by running:
```bash
poetry install
poetry run pre-commit run --all-files
```

Additionally on every `git commit` the hooks will be triggered and have to pass.

#### How to run tests

You can run all the tests, by simply running:
```bash
poetry install
poetry run pytest -vv
```

## Support & Feedback

Your contribution is very much appreciated. Feel free to create a PR or an Issue with your suggestions for improvements.
