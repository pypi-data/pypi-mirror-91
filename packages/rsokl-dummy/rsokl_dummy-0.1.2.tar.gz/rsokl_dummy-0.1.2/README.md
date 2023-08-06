# Dummy_Repo

[![Automated tests status](https://github.com/mitll-SAFERai/example-python-project/workflows/Tests/badge.svg)](https://github.com/mitll-SAFERai/example-python-project/actions?query=workflow%3ATests+branch%3Amain)
[![PyPi version status](https://img.shields.io/pypi/v/rsokl_dummy.svg)](https://pypi.python.org/pypi/rsokl_dummy)
[![Docs](https://github.com/mitll-SAFERai/example-python-project/workflows/github%20pages/badge.svg)](https://github.com/mitll-SAFERai/example-python-project/actions?query=workflow%3A%22github+pages%22)


## GitHub Actions

This repo exercises the following GitHub actions:
- [Automated tests and code-coverage measures](https://github.com/mitll-SAFERai/example-python-project/blob/main/.github/workflows/tox_run.yml)
  - Uses `tox` and the [`tox GitHub Actions recipe`](https://github.com/ymyzk/tox-gh-actions) to run the repo's tests against
  Python versions 3.6, 3.7, and 3.8
  - Runs measures code-coverage of tests under Python 3.7 (gates on 100% coverage for this repo)
  - These jobs run whenever there is any push or PR into the `main` or `develop` branches; PRs will also be gated by the passing statuses of these jobs
  (see the [blocked PRs](https://github.com/mitll-SAFERai/example-python-project/pulls) where the tests where made to fail). These settings can be adjusted in the `.github/workflows/tox_tun.yml` file.
- [Publishing the project wheel to pypi whenever new release is created](https://github.com/mitll-SAFERai/example-python-project/blob/main/.github/workflows/pypi_publish.yml)
  - You must save your pypi username and password as [secrets associated with the repo](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)
  (available under the repo's settings, to the repo owner) as `PYPI_USERNAME` and `PYPI_PASSWORD` respectively. (Note that these will be encrypted)
  - This action will publish to pypi any time you [create a new release](https://github.com/mitll-SAFERai/example-python-project/releases/tag/v0.1.1); i.e. this
  new release will become available to users via `pip install rsokl_dummy`
- [Publishing docs whenever the `main` branch gets updated](https://github.com/mitll-SAFERai/example-python-project/blob/main/.github/workflows/publish_docs.yml)
  - The resulting website can be viewed [here](https://mitll-saferai.github.io/example-python-project/)
  - The `main` branch only houses the configuration and "plain text" source files for the documentation
  - The "action" is responsible for installing `sphinx` (and other dependencies specified in `docs/requirements.txt`), running sphinx, and
  publishing the resulting HTML to a separate `gh-pages` branch
    - The present sphinx configuration (in `docs/conf.py`) specifies that the `source` and `build` directory be kept separate
    - Under the repositories `Settings`, be sure to specify the "GitHub Pages" source branch to `gh-pages`, and the associated
    directory to `docs/`, if you are copying the configuration from this repo

## This project's approach to versioning

This project leverages [versioneer](https://github.com/python-versioneer/python-versioneer) to manage its versioning.
In effect, this means that the git-tag & commit-hash associated with the repo-branch determines the version returned by `rsokl_dummy.__version__`.
This makes versioning more precise, descriptive, and useful, as each commit will have a distinct version string. This is in
stark contrast to projects that manually maintain a version string, where often times a wide range of project iterations can all fall under 
the umbrella of a single version – where asking "well what version are you using" becomes an uninformative question. 

 