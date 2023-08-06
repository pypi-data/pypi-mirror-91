# Faros Python Client

_Python client for the [Faros](https://www.faros.ai) API_

## Documentation

Please read the [Faros documentation][farosdocs] to learn more. See also our [apps repo][farosapps] for examples to help you get started.

[farosdocs]: https://www.faros.ai/docs
[farosapps]: https://github.com/faros-ai/faros-apps

## Developing

```sh
$ pip install -r requirements.txt
```

We currently using flake8 for linting so ensure your code editor is using that
for linting. You can also run `flake8 . --count --show-source --max-complexity=10 --max-line-length=120 --statistics`

> :memo: NOTE: Note: In the future will switch to something like [black](https://black.readthedocs.io/en/stable/) to automatically format on commit.

> :memo: If you add new packages to the client, also add them to `install_requires` section in [setup.py](setup.py), to ensure their added to packaged client published to [PyPi](https://pypi.org/project/faros)

## Releasing

To release a new version of the client first bump the version in [init file](faros/__init__.py).

1. From the repo's home page, click on "releases" then "Draft a new release".
2. In the "Tag version" input, select the tag corresponding to the version you want to release from the auto-complete or type in to create a new version
3. Enter a release title and description, check the pre-release box if appropriate, and click "Publish release".

The `Publish to PyPi` workflow in this repository will then automatically
publish the code to PyPi. If all goes well, you be able to see it shortly
after [here](https://pypi.org/project/faros) with the new version.
