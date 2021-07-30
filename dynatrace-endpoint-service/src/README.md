# Welcome to the Dynatrace Endpoint Service AWS CDK Project

This application has been written with [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html). After cloning the repo the project will need a few configuration steps before it is usable.

## Configure AWS CDK local environment

After cloning the repo this AWS CDK project will need a couple of steps to become useable. The Python virtual environment will need to be initialised and updated with project libraries and dependencies.

The version requirements are controlled in `src/setup.py`; your system Python will need to be version 3.6 or greater. Check this with `python3 --version`

*Snippet from `src/setup.py`*

```python
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
```

Navigate to the root of the project and create a new Python virtual environment:

```bash
 python3 -m venv .venv
```

Activate the virtual environment with the following command.

```bash
source .venv/bin/activate
```

All python-related paths are now pointing to the local Python environment. The app's dependencies can be installed with:

```bash
python -m pip install -r requirements.txt
```

## Locally testing commits

Pre-commit hooks are included with the repo and will need initialising before you will be able to commit any changes.

```bash
pre-commit install
```

If any files are modified automatically by Pre-commit tasks the changes will need to be staged again in Git. Re-committing the changes after staging them in Git should now get you some way towards uploading your branch. The following tests and checks have been added to the repository:

Pre-commit test                 | Function
:----                           | :----
Pre-commit hooks                | A series of checks and auto-fixes for json, yaml and Python files
Black                           | 'Uncompromising' Python code formatter
Pylint                          | Python Linting and error detection

### Using pre-commit

The test suite configured under Pre-commit will run every time a `git commit` is executed. The same tests can also be run at any time with the following command from the root directory of the project:

```bash
pre-commit run
```

Expected Output:

```bash
(.venv) ➜ pre-commit run
Check for case conflicts..................................................Passed
Check JSON............................................(no files to check)Skipped
Check for merge conflicts.................................................Passed
Check for broken symlinks.............................(no files to check)Skipped
Check Yaml............................................(no files to check)Skipped
Fix End of Files..........................................................Passed
Trim Trailing Whitespace..................................................Passed
Mixed line ending.........................................................Passed
unittest..................................................................Passed
```

### Unittest

Unittest is being used to check the application templates before pushing to GitHub. This is still in development but this can be manually run by executing the following command from the root of the application directory:

```bash
(.venv) ➜ python3 -m unittest test.test_unittest_dynatrace_activegate -v
```

This is currently under development and may use different libraries in the future.
