# Setup

## Installation

Zensical is published as a Python package on PyPI. Use a virtual environment.

### Install with pip

```sh
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install zensical

# Windows
python -m venv .venv
.venv\Scripts\activate
pip install zensical
```

### Install with uv

```sh
uv init
uv add --dev zensical
```

### Docker

An official Docker image is available on Docker Hub at `zensical/zensical`.

---

## Create a New Project

```sh
zensical new .
```

This generates:

```sh
.
├─ .github/
├─ docs/
│  ├─ index.md
│  └─ markdown.md
└─ zensical.toml
```

- `zensical.toml` — project configuration
- `docs/` — Markdown source files (configurable via `docs_dir`)
- `.github/` — GitHub Actions workflow for automatic deployment

---

## CLI Commands

```sh
zensical COMMAND [OPTIONS]
```

| Command | Description |
| --- | --- |
| `zensical new PROJECT_DIRECTORY` | Create a new project |
| `zensical build [OPTIONS]` | Build static site |
| `zensical serve [OPTIONS]` | Start local preview server |

### Build options

| Option | Short | Description |
| --- | --- | --- |
| `--config-file` | `-f` | Path to config file |
| `--clean` | `-c` | Clean cache |
| `--help` | | Show help |

### Serve options

| Option | Short | Description |
| --- | --- | --- |
| `--config-file` | `-f` | Path to config file |
| `--open` | `-o` | Open in default browser |
| `--dev-addr IP:PORT` | `-a` | Bind address (default: localhost:8000) |
| `--help` | | Show help |

---

## Configuration File

Zensical uses `zensical.toml` (recommended) or `mkdocs.yml` (compatibility). All settings live under the `[project]` scope in TOML.

### Required settings

```toml
[project]
site_name = "My Site"
```

### Common settings

```toml
[project]
site_name = "My Site"
site_url = "https://example.com"
site_description = "A description of my site."
site_author = "Jane Doe"
copyright = "&copy; 2025 Jane Doe"
docs_dir = "docs"
site_dir = "site"
repo_url = "https://github.com/example/repo"
repo_name = "example/repo"
use_directory_urls = true
dev_addr = "localhost:8000"
```

### Navigation

```toml
[project]
nav = [
  "index.md",
  {"About" = "about.md"},
  {"Section" = [
    "section/index.md",
    {"Page 1" = "section/page-1.md"}
  ]}
]
```

External links: any nav value that is not a Markdown path is treated as a URL.

---

## Theme Variant

```toml
[project.theme]
variant = "modern"   # or "classic" (matches Material for MkDocs look)
```

---

## Publishing

### GitHub Pages (GitHub Actions)

Create `.github/workflows/docs.yml`:

```yaml
name: Documentation
on:
  push:
    branches:
      - master
      - main
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/configure-pages@v5
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with:
          python-version: 3.x
      - run: pip install zensical
      - run: zensical build --clean
      - uses: actions/upload-pages-artifact@v4
        with:
          path: site
      - uses: actions/deploy-pages@v4
        id: deployment
```

### GitLab Pages

Create `.gitlab-ci.yml`:

```yaml
pages:
  stage: deploy
  image: python:latest
  script:
    - pip install zensical
    - zensical build --clean
  pages:
    publish: public
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

Set `site_dir = "public"` in your configuration for GitLab.

---

## Upgrading

```sh
# pip
pip install --upgrade --force-reinstall zensical

# uv
uv lock --upgrade-package zensical==<version>
```

Check the [changelog](https://github.com/zensical/zensical/releases) for release notes.

---

## Offline Usage

```toml
[project.plugins.offline]
```

Enables client-side search when the site is distributed as a download (accessed from the filesystem). Disable instant navigation, analytics, git repository info, and comment systems when building for offline use.