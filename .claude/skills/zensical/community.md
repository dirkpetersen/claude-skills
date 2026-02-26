# Community

## Contributing

Before opening an issue or pull request, review the contribution guidelines.

### Issue types

- **Bug report** — Something is not working correctly
- **Docs issue** — Missing or incorrect documentation
- **Change request** — Feature request or improvement proposal
- **Discussion** — Questions (use Discord, not the issue tracker)

### Before creating an issue

1. Upgrade to the latest version of Zensical
2. Remove customizations (`custom_dir`, `extra_css`, `extra_javascript`) to isolate the problem
3. Search existing issues and documentation

---

## Bug Reports

A good bug report includes:

- **Title** — Short, descriptive, one sentence (e.g. `Built-in typeset plugin changes nav title precedence`)
- **Context** (optional) — Relevant circumstances
- **Bug description** — What is wrong, why it is a bug, one bug per issue
- **Related links** — Docs sections, related issues
- **Reproduction** — A minimal `.zip` file reproduction (not a repository link)
- **Steps to reproduce** — Exact steps to observe the bug
- **Browser** (optional) — If browser-specific

### Creating a reproduction

```sh
zensical new reproduction
cd reproduction
# Add minimal config and content to reproduce the issue
pip freeze > requirements.txt
# Pack into .zip and attach to GitHub issue
```

---

## Documentation Issues

Report at the docs issue tracker. Include:

- **Title**
- **Description** — What is wrong or missing
- **Related links** — Links to the affected pages
- **Proposed change** (optional) — Suggested improvement

---

## Change Requests

Before submitting:

1. Verify it is not a bug
2. Look for similar implementations elsewhere
3. Discuss on Discord to gauge community interest

A change request includes: title, context, description, related links, use cases, visuals (optional).

After submission, the Zensical team reviews and may move accepted ideas to the public backlog.

---

## Pull Requests

1. Open an issue and discuss the approach before starting work
2. Follow coding style (Rust: rustfmt + clippy; Python: ruff + mypy; TypeScript: typescript-eslint)
3. Sign commits with GPG/SSH (`git commit -s`) — Developer Certificate of Origin required
4. Use Conventional Commits format:

```
<type>: <summary description> (#<issue number>)

Signed-off-by: Name <email>
```

Accepted commit types: `feature`, `fix`, `performance`, `refactor`, `build`, `docs`, `style`, `test`, `chore`.

5. Do not include AI-generated code you cannot fully explain

---

## Code of Conduct

All community spaces (GitHub, Discord, Zensical Spark, email) require respectful, inclusive behavior.

**Accepted behavior:** welcoming language, respecting differing viewpoints, gracefully accepting criticism, showing empathy.

**Unaccepted behavior:** harassment, trolling, publishing private information, sexual language or imagery.

Violations: first warning → second warning (5-day reflection period) → restriction or blocking.

Report violations to hello@zensical.org.

---

## Community Channels

- **Discord** — Community-driven Q&A and discussion: https://discord.gg/hqXRNq9CjT
- **GitHub Issues** — Bug reports, docs issues, change requests: https://github.com/zensical/zensical
- **Zensical Spark** — Professional support and design collaboration: https://zensical.org/spark/
- **Public backlog** — Track planned work: https://github.com/orgs/zensical/projects/2
- **Public roadmap** — Project direction: https://zensical.org/about/roadmap/