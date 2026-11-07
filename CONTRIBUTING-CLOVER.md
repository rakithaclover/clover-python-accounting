# Maintaining clover-python-accounting

How this distribution is kept, released and, if needed, published. For contributing to the library itself, see
`CONTRIBUTING`.

## What may be in this repository

This repository is **public**. Before every push, check that the diff contains only:

- library code under `python_accounting/`, its tests under `tests/`, and its documentation;
- the packaging files of this distribution (`pyproject.toml`, `poetry.lock`, `NOTICE.md`, this file, the
  README notice, `.github/workflows/clover-*.yml`).

Never: application code, schemas or migrations of any product using the library, configuration, credentials,
internal host names or URLs, customer, business or market data, or the name of any company other than Clover.
Test data stays generic.

## Identity

Commits are authored with the GitHub account's no-reply e-mail, set in this repository only:

```bash
git config user.name  "rakithaclover"
git config user.email "192121035+rakithaclover@users.noreply.github.com"
```

On GitHub → Settings → Emails, "Keep my email addresses private" and "Block command line pushes that expose my
email" are on.

## Branches

| Branch | Content |
|---|---|
| `main` | The original project's `main` (GitHub "Sync fork") |
| `fix/<id>-<name>` | One change each, from upstream `main`, with its test. Offered upstream as a pull request |
| `clover/<upstream minor>` | The upstream release + the changes not yet released upstream (cherry-picked with `-x`) + the packaging commit |

## Making a change

1. Branch `fix/<id>-<name>` from `main`. Write the test first and see it fail.
2. Fix it in the form upstream can accept: existing behaviour and stored data unchanged by default, a setting
   where the change would alter stored data.
3. `pylint ./python_accounting` (10.00/10) and `pytest` must pass; `CHANGELOG` is left to the upstream maintainer.
4. Open an issue upstream (what happens, a minimal reproduction, the proposed fix), then a pull request from the
   branch. Record both links in `NOTICE.md`.
5. Cherry-pick the commit onto `clover/<minor>` with `git cherry-pick -x`.

## Releasing

1. On `clover/<minor>`, set `version` in `pyproject.toml` to `<upstream version>.<n>` and add the release to
   `NOTICE.md`.
2. Tag `v<version>` and push the tag. `clover-release.yml` runs the tests (SQLite and PostgreSQL), builds the wheel
   and sdist, runs `twine check`, and attaches both with their SHA-256 sums to a GitHub release.
3. Consumers copy the wheel from the release and pin it by its hash.

Nothing is uploaded to PyPI by a release.

## When upstream releases

Create `clover/<new minor>` from the new upstream tag, cherry-pick only the changes upstream did not take, re-apply
the packaging commit, release `<new version>.1`, and mark the merged changes in `NOTICE.md`.

## Publishing to PyPI (prepared, off)

Publish only if the original project has had no release or maintainer response for six months **and** a change is
needed that it has not taken. Then:

1. On PyPI, add a pending trusted publisher for `clover-python-accounting`: owner `rakithaclover`, repository
   `clover-python-accounting`, workflow `clover-publish.yml`, environment `pypi`.
2. In this repository, create the environment `pypi` with a required reviewer.
3. Run **clover-publish** by hand with the release tag; approve it.
4. Update the README notice and open an issue upstream pointing to this distribution.

Until then `clover-publish.yml` cannot publish: no trusted publisher exists for it on PyPI.
