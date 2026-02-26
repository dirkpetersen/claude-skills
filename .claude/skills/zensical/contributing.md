# Contributing

## Community Channels

- GitHub Issues: bug reports, docs issues, change requests
- Discord: community discussion, questions
- Zensical Spark: professional support, design process participation

## Reporting Bugs

### Before Filing

1. Upgrade to the latest version.
2. Remove customizations (`custom_dir`, `extra_css`, `extra_javascript`).
3. Search docs and issue tracker for existing reports.

### Issue Fields

- **Title**: short one-sentence executive summary
- **Context** (optional): circumstances of use
- **Bug description**: what is wrong, not how to reproduce
- **Related links**: docs sections and prior issues
- **Reproduction**: minimal `.zip` file (see below)
- **Steps to reproduce**: step-by-step with simple language
- **Browser** (optional): name and version if browser-specific

### Creating a Minimal Reproduction

```sh
zensical new reproduction
cd reproduction
# add minimal content that reproduces the bug
pip freeze > requirements.txt
# remove site/ directory, then zip
```

## Documentation Issues

File on the docs repository issue tracker. Include:

- Title
- Description (what is wrong or missing)
- Related links (use anchor/permanent links)
- Proposed change (optional)

## Change Requests

File on the main issue tracker. Include:

- Title
- Context (optional)
- Description (what, not why)
- Related links
- Use cases (who benefits, how many users, breaking changes?)
- Visuals (optional)

Changes go through: issue → backlog item → design document → implementation → PR.

## Pull Requests

### Before Starting

Open an issue and discuss the approach before writing code.

### Requirements

| Language | Linting/Formatting |
|----------|--------------------|
| Rust | rustfmt + clippy |
| Python | ruff + mypy |
| TypeScript | typescript-eslint |

Use `.editorconfig` settings. All commits must be cryptographically signed (GPG, SSH, or S/MIME).

### Developer Certificate of Origin

Add `-s` flag to every commit:

```sh
git commit -s -m "fix: correct admonition rendering (#123)"
```

### Commit Message Format

```
<type>: <summary description> (#<issue number>)

Signed-off-by: ...
```

Accepted types: `feature`, `fix`, `performance`, `refactor`, `build`, `docs`, `style`, `test`, `chore`.

Rules:
- Lowercase summary, no trailing punctuation
- Issue number in parentheses with no whitespace inside
- No extra whitespace

### Use of Generative AI

AI-assisted code is permitted only if you have thoroughly reviewed and fully understand it. Unreflected AI-generated code will be rejected.

## Code of Conduct

Expected behavior: welcoming language, respecting differing viewpoints, gracefully accepting criticism, empathy.

Unacceptable: harassment, trolling, personal attacks, publishing private information.

Scope: GitHub repos, Discord, social media, Zensical Spark, email.

Violations: first warning → second warning (5-day reflection period) → restriction or block.

Report violations to hello@zensical.org.