# NOTICE — clover-python-accounting

**clover-python-accounting** is a maintained distribution of
[python-accounting](https://github.com/ekmungai/python-accounting), maintained by Clover.

- Original work: Copyright (c) 2024 Edward Mungai, released under the MIT License (see [LICENSE](LICENSE)).
- Changes listed below: Copyright (c) 2026 the Clover contributors, released under the same MIT License.

The import name is unchanged (`python_accounting`). Install either this distribution or `python-accounting`, not
both.

## Base

| Item | Value |
|---|---|
| Upstream repository | https://github.com/ekmungai/python-accounting |
| Upstream release | 2.1.0 (PyPI `python-accounting` 2.1.0) |
| Upstream tag and commit | `v2.1.0`, `1fcf6ec2e8ed25519f7228401acf5c687bae2015` (the tag's `python_accounting/` and `config.toml` are identical to the PyPI 2.1.0 wheel, checked 2026-11-07) |
| This branch | `clover/2.1` |

## Changes

Each change is a separate branch, offered to the original project as a pull request. When an upstream release
contains a change, it is dropped from this distribution.

| # | Change | Branch | Upstream issue | Upstream pull request | Status |
|---|---|---|---|---|---|
| D0 | Session listeners are registered on `AccountingSession` only, so other sessions in the application are not affected | `fix/d0-session-listeners` | — | — | not yet offered |
| D1 | `mysqlclient` and `psycopg2` are the optional extras `mysql` and `postgresql` | `fix/d1-optional-db-drivers` | — | — | not yet offered |
| D2 | `created_at` and `updated_at` are taken when records are saved and updated, not at import | `fix/d2-timestamp-defaults` | — | — | not yet offered |
| D3 | Opt-in hash chain `chain = "entity"`: each Ledger record chains to the previous Ledger record of its Entity (default `"legacy"` unchanged) | `fix/d3-ledger-hash-chain` | — | — | not yet offered |
| D4 | Opt-in `amount_precision` for amount and quantity columns (default 13 unchanged) | `fix/d4-amount-precision` | — | — | not yet offered |
| D5 | Moving the current Reporting Period flushes instead of committing the caller's session | `fix/d5-no-commit-in-listener` | — | — | not yet offered |

Packaging (this distribution only, not offered upstream): distribution name `clover-python-accounting`, versions
`<upstream version>.<n>`, this notice, the README notice, `CONTRIBUTING-CLOVER.md`, the `clover-*` workflows, and
`tests/postgresql/smoke.py`.

## Releases

| Version | Base | Changes |
|---|---|---|
| 2.1.0.1 | python-accounting 2.1.0 | D0–D5 |

## Package name

| Name | PyPI, checked 2026-11-07 |
|---|---|
| `clover-python-accounting` (used) | not registered |
| `clover-accounting-engine` (fallback) | not registered |
| `python-accounting-clover` (fallback) | not registered |

This distribution is not published on PyPI. See `CONTRIBUTING-CLOVER.md` for when and how it would be.
