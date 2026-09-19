# Using django-nx with AI coding agents

django-nx ships a version-matched API contract as `nx/ai_context.md`. Add one of
the following rules to a consuming project so its coding agent reads that
contract before editing Django models or DRF code.

The contract path can be resolved without importing Django or configuring
settings:

```bash
python -c 'from importlib.metadata import distribution; print(distribution("django-nx").locate_file("nx/ai_context.md"))'
```

## AGENTS.md or CLAUDE.md

```md
## django-nx

This project uses django-nx. Before changing Django models, serializers,
viewsets, or routes, locate and read its installed API contract:

python -c 'from importlib.metadata import distribution; print(distribution("django-nx").locate_file("nx/ai_context.md"))'

Use `import nx` and prefer APIs documented there. Do not inspect django-nx
implementation source unless the contract does not cover the required behavior
or you are diagnosing a django-nx defect.
```

## Cursor project rule

Create `.cursor/rules/django-nx.mdc` in the consuming project:

```md
---
description: Use the installed django-nx public API contract
globs:
  - "**/*.py"
alwaysApply: false
---

When working with Django models or Django REST Framework, locate and read the
installed `nx/ai_context.md` using `importlib.metadata.distribution("django-nx")`.
Use `import nx` and documented public APIs. Inspect django-nx implementation
only when its API contract is insufficient or when diagnosing a library defect.
```

## Web-only agents

If the agent cannot access the Python environment, direct it to:

- `https://raw.githubusercontent.com/JoshYuJump/django-nx/main/llms.txt`
- `https://raw.githubusercontent.com/JoshYuJump/django-nx/main/nx/ai_context.md`

The installed contract should take precedence when the application pins an
older django-nx version.
