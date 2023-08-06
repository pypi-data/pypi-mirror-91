# pypi-dist

Convenience script for distributing projects to PyPi

## Usage

Execute from the root of the git repository.

```
Usage: pypi_dist.py [OPTIONS]

Options:
  --release-type [major|minor|patch]
                                  The increment type of this version
  --version TEXT                  A specific version number to release
  --pypi-username TEXT            The username for the pypi account to upload
                                  to

  --pypi-password TEXT            The password for the pypi account to upload
                                  to

  --help                          Show this message and exit.
```


PyPi credentials can be resolved in several ways:

1) Using `--pypi-username` / `--pypi-password`
1) Through the `PYPIDIST_USERNAME` / `PYPIDIST_PASSWORD` environment variables.
1) Through a valid `.pypirc` file in your home directory.