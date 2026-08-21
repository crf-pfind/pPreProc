# Documentation maintenance

The English and Simplified Chinese sites are independent Sphinx projects with
matching page paths.

```text
docs/en/       English source and Sphinx configuration
docs/zh_CN/    Simplified Chinese source and Sphinx configuration
```

## Local builds

From the repository root:

```console
python -m pip install -r docs/requirements.txt
python -m pip install .
sphinx-build -W --keep-going -b html docs/en build/docs/en
sphinx-build -W --keep-going -b html docs/zh_CN build/docs/zh-cn
```

`python tools/check_repository.py` also checks that both languages contain the
same document paths.

## Read the Docs

The English project uses the root `.readthedocs.yaml`. In the Simplified
Chinese project, set **Admin > Settings > Build configuration file** to:

```text
docs/zh_CN/.readthedocs.yaml
```

Then set the Chinese project as a translation of the English project and build
`latest` in both projects. The public routes are:

- `https://ppreproc.readthedocs.io/en/latest/`
- `https://ppreproc.readthedocs.io/zh-cn/latest/`

Enable **Settings > Pull request builds** for both projects to receive rendered
documentation previews on pull requests.
