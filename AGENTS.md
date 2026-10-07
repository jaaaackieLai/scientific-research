# AGENTS.md

## Versioning

The plugin version lives only in `.claude-plugin/marketplace.json` (`plugins[0].version`).

- Add or remove a skill, or add behavior to one: bump minor (`0.5.2` → `0.6.0`).
- Fix or reword without new behavior: bump patch (`0.6.0` → `0.6.1`).

## Release flow: merge first, release from main

1. Bump the version in the PR that ships the change.
2. Merge the PR to `main`. That is the release: users pick it up from `main` with the update commands in `README.md`.

Do not create GitHub tags or Releases; nothing reads them.
