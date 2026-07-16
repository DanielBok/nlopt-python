---
name: update-nlopt
description: Bump the vendored nlopt C library (extern/nlopt submodule) to a new upstream release, and understand how that flows through to a PyPI publish. Use when asked to "update nlopt", "bump nlopt version", or similar.
---

# Updating the vendored nlopt version

This package wraps the upstream C library [nlopt](https://github.com/stevengj/nlopt),
vendored as the `extern/nlopt` git submodule. The Python package version is **not**
tracked separately — `setup.py` derives it at build time by regex-parsing
`NLOPT_MAJOR_VERSION` / `NLOPT_MINOR_VERSION` / `NLOPT_BUGFIX_VERSION` out of
`extern/nlopt/CMakeLists.txt`. There is no `pyproject.toml` version, no `__init__.py`
version, nothing else to edit for a routine bump.

## 1. Bump the submodule to a specific release tag

Pin to an exact upstream tag rather than `git submodule update --remote` (which floats
to the tip of whatever branch the submodule tracks, potentially landing on unreleased
commits past the last tag):

```shell
cd extern/nlopt
git fetch --tags
git tag --list "v*" --sort=-v:refname | head   # find the latest release tag
git checkout vX.Y.Z
cd ../..
git add extern/nlopt
git commit -m "Bump nlopt submodule to vX.Y.Z"
```

Sanity-check the version macros landed correctly:

```shell
grep -oP 'NLOPT_(MAJOR|MINOR|BUGFIX)_VERSION *"\K[^"]+' extern/nlopt/CMakeLists.txt
```

This should print the three version components matching the tag you checked out —
this is exactly what `setup.py` and the CI "already published on PyPI" guard
(`.github/workflows/wc-build.yml`, "Ensure version is not already published on PyPI"
step) both parse to compute the package version.

## 2. Check whether CI's OS/Python matrix needs touching

Almost never required for a routine nlopt bump — only if the new release changes which
Python versions or platforms are supported:

- `.github/workflows/build.yml` — `os` / `python-versions` inputs passed to the
  reusable `wc-build.yml`, used for PR builds and release-triggered publishes.
- `.github/workflows/manual-deploy.yml` — the same OS/Python choices, exposed as
  `workflow_dispatch` checkboxes for on-demand testpypi/pypi builds.

There is no manylinux Dockerfile step anymore (CI uses the prebuilt
`quay.io/pypa/manylinux_2_28_x86_64` / `..._aarch64` images directly in
`wc-build.yml`) and no hardcoded `CIBW_BUILD` list to hand-edit — it's derived
from the `python-versions` input.

## 3. Verify via CI, not locally

Push the branch and open a PR against `master`. `build.yml`'s `pull_request` trigger
runs `wc-build.yml` with `target: none`, which builds wheels across the full OS/Python
matrix and runs `extern/nlopt/test/t_python.py` against each installed wheel — this is
the real regression check. `test_scripts/sample_test_script.py` is available as an
optional extra manual smoke test if you want to exercise a specific solver locally.

## 4. Optional dry-run publish

Trigger `manual-deploy.yml` via `workflow_dispatch` with `target: testpypi` to validate
the full build+upload path (including the version-suffix auto-generation for testpypi's
14-day immutability rule) before a real release.

## 5. Real release

Cut a GitHub Release (tag `vX.Y.Z`, matching the nlopt version). `build.yml`'s
`release: published` trigger runs `wc-build.yml` with `target: pypi`, which builds,
tests, and publishes via trusted OIDC publishing — no manual `twine upload` needed.
