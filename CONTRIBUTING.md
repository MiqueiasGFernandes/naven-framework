# Contributing to Naven

Thank you for helping improve Naven. The project is experimental and its API is
still taking shape, so contributions that keep behavior explicit, reliable, and
easy to operate in production are especially valuable.

## Before you start

- Check the existing issues and pull requests to avoid duplicating work.
- Open an issue before a large change, a new dependency, or a public API or
  architecture change. This gives maintainers and contributors a chance to
  agree on the direction before implementation begins.
- Keep each contribution focused. Separate unrelated refactors from functional
  changes whenever possible.

## Set up the project

Naven requires Python 3.11 or newer and uses
[`uv`](https://docs.astral.sh/uv/) to manage the development environment.

Fork and clone the repository, then install all dependency groups:

```bash
uv sync --locked --all-groups
```

Install the Git hooks if you want the same automatic checks used by the
project:

```bash
uv run pre-commit install
```

## Make a change

- Add or update tests for every behavior change and bug fix.
- Preserve support for all Python versions declared in `pyproject.toml`.
- Keep public APIs typed and document user-visible behavior.
- Prefer small, composable changes that follow the production-first principles
  and operation semantics described in the README.
- Avoid adding a dependency when the standard library or a small local
  implementation is sufficient. Explain the trade-off when a new dependency
  is necessary.

The examples in the README include proposed APIs that may not exist yet. Do
not assume an example is implemented without checking the source and tests.

## Architecture decisions

Changes that affect the framework contract, cross-cutting runtime behavior, or
multiple architectural layers should include an Architecture Decision Record.
Read the [ADR index and process](docs/adr/README.md), then start from the
[ADR template](docs/adr/template.md). Small, local, and easily reversible
implementation choices do not require an ADR.

## Run the checks

Before opening a pull request, run the same checks as CI:

```bash
uv run --no-sync ruff check .
uv run --no-sync ruff format --check src tests
uv run --no-sync pytest
uv build --no-sources
```

To apply Ruff's safe fixes and formatting locally, run:

```bash
uv run ruff check --fix .
uv run ruff format src tests
```

## Commit and open a pull request

Use clear, focused commit messages. The repository follows Conventional
Commits-style prefixes, for example:

```text
feat: add ASGI application callable
fix: preserve request context during cancellation
docs: clarify deadline propagation
test: cover duplicate route detection
```

In the pull request:

- explain the problem and the chosen solution;
- link the related issue, if one exists;
- call out compatibility or operational consequences;
- include tests and documentation needed to review the change; and
- confirm that the checks above pass.

Contributions are licensed under the [MIT License](LICENSE).
