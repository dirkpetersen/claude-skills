# Contributing

## Before Creating an Issue

- Use the latest version of Zensical (bugs are not backported)
- Remove customizations (`custom_dir`, `extra_css`, `extra_javascript`) to rule them out
- Search existing issues and documentation
- Use `--clean` flag if you encounter unexpected build behavior after upgrading

## Bug Reports

Include:
- **Title**: short, descriptive one-sentence summary
- **Context**: circumstances (optional)
- **Bug description**: clear explanation of what is wrong (not how to reproduce)
- **Related links**: docs sections, existing issues
- **Reproduction**: minimal `.zip` file created with `zensical new reproduction`
- **Steps to reproduce**: exact steps to observe the bug
- **Browser**: if browser-specific (optional)
- **Checklist**: confirm all fields complete

### Creating a reproduction

```sh
zensical new reproduction
cd reproduction
# Add minimal config and content to reproduce the bug
pip freeze > requirements.txt
# Remove non-essential files, then zip
```

## Documentation Issues

Include: title, description of inconsistency, related links, proposed change (optional).

## Change Requests

Before submitting:
- Verify it is not a bug report
- Look for prior art in other tools
- Discuss on Discord first

Include: title, context (optional), description, related links, use cases, visuals (optional).

### How change requests are managed

1. Team reviews the request
2. If in scope, moved to public backlog
3. Original issue closed (linked to backlog item)
4. Design documents published before development
5. Community invited to give feedback and contribute PRs

## Pull Requests

Requirements:
- Open an issue and discuss before starting work
- Reference the issue in the PR
- Follow code style (rustfmt, clippy, ruff, mypy, typescript-eslint)
- Use `.editorconfig`-compatible editor settings
- Sign commits (GPG, SSH, or S/MIME)
- Add `Signed-off-by` trailer: `git commit -s`
- Follow Conventional Commits format

### Commit message format

```
<type>: <summary description> (#<issue number>)

Signed-off-by: Name <email>
```

| Type | Description |
| --- | --- |
| `feature` | New feature |
| `fix` | Bug fix |
| `performance` | Performance improvement |
| `refactor` | Code improvement without behavior change |
| `build` | Build/CI changes |
| `docs` | Documentation |
| `style` | Stylistic changes only |
| `test` | Tests |
| `chore` | Build process, release prep |

### Use of Generative AI

By signing off, you attest that you have either written all code yourself or thoroughly reviewed and fully understood any generated code. AI-generated code that cannot be explained will be rejected.

## Code of Conduct

The Zensical community expects all participants to:
- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Show empathy toward others

Unacceptable behavior (harassment, personal attacks, publishing private info, etc.) may result in warnings, access restrictions, or blocking.

Report violations to: hello@zensical.org

### Warning policy

1. **First warning**: permanent formal notice
2. **Second warning**: 5-day reflection period to respond/apologize
3. **Restriction or blocking**: if no improvement after second warning

## Community Channels

- **Discord**: community-driven Q&A, tips, discussion
- **GitHub Issues**: bug reports, change requests (not questions)
- **Zensical Spark**: professional support, design process participation