# Copilot Instructions for Ploosh

## Context
- Ploosh is a YAML-based data testing framework.
- Main code lives in `src/ploosh`.
- Tests live in `tests` and run with `pytest`.
- Documentation lives in `docs`.

## Language and Style
- Write comments and documentation in English.
- Keep changes focused and minimal: only touch files related to the request.
- Preserve existing APIs and naming unless the request explicitly asks for breaking changes.
- Follow the existing project style (imports, class naming, connector patterns).

## Python Guidelines
- Target Python code under `src/ploosh`.
- Prefer clear, explicit error messages (`ValueError` with actionable context).
- Avoid adding new dependencies unless strictly necessary.
- Reuse existing connector and engine patterns before introducing new abstractions.

## Testing and Validation
- Run relevant tests first, then broader tests if needed.
- Typical command:

```bash
pytest
```

- For connector changes, prioritize tests in `tests/connectors`.
- For compare/load behavior changes, run tests in `tests/compare_engine` and `tests/load_engine`.

## Documentation Expectations
- If behavior or configuration changes, update docs in `docs` in the same change.
- For connector option changes, update the relevant connector page and related usage examples.
- Keep examples realistic and consistent with actual parameter names.

## Commit Message Guidelines
- Use conventional commits format: `<type>(<scope>): <description>`.
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
- Scope is optional and should refer to the impacted area (for example `connector`, `compare-engine`, `load-engine`, `docs`).
- Description must be concise and under 72 characters.
- Split large or mixed changes into multiple focused commits when possible.

## Pull Request Quality Bar
- Include tests for new logic or bug fixes when feasible.
- Avoid unrelated refactors in feature or fix PRs.
- Ensure code and docs remain consistent before finalizing.
- Follow the PR template in `.github/pull_request_template.md` when describing changes.