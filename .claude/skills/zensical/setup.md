# Setup

## Installation

Zensical is distributed as a Python package. Use a virtual environment.

### With pip

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install zensical
```

On Windows:

```ps1
python -m venv .venv
.venv\Scripts\activate
pip install zensical
```

### With uv

```sh
uv init
uv add --dev zensical
```

### Docker

An official Docker image is available on Docker Hub at `zensical/zensical`.

## Create a New Project

```sh
zensical new .
```

Generated structure:

```sh
.
├─ .github/
├─ docs/
│  ├─ index.md
│  └─ markdown.md
└─ zensical.toml
```

- `zensical.toml` — project configuration
- `docs/` — Markdown source files (`docs_dir`)
- `.github/` — GitHub Actions workflow for Pages deployment

## Configuration File Formats

Zensical reads both `zensical.toml` (recommended for new projects) and `mkdocs.yml` (for migration from Material for MkDocs).

### Minimal zensical.toml

```toml
[project]
site_name = "My site"
site_url = "https://example.com"
```

### Minimal mkdocs.yml

```yaml
site_name: My site
site_url: https://example.com
```

## Core Settings

### site_name (required)

```toml
[project]
site_name = "My Zensical project"
```

### site_url

Required for instant navigation, instant previews, and custom error pages.

```toml
[project]
site_url = "https://example.com"
```

### site_description

```toml
[project]
site_description = "Lorem ipsum dolor sit amet."
```

### site_author

```toml
[project]
site_author = "Jane Doe"
```

### copyright

```toml
[project]
copyright = "&copy; 2025 Jane Doe"
```

### docs_dir

```toml
[project]
docs_dir = "docs"
```

### site_dir

```toml
[project]
site_dir = "site"
```

### use_directory_urls

Controls URL format. Defaults to `true`.

```toml
[project]
use_directory_urls = false
```

| Value | Source file | URL |
|-------|-------------|-----|
| true | usage.md | /usage/ |
| false | usage.md | /usage.html |

### dev_addr

```toml
[project]
dev_addr = "localhost:3000"
```

Default: `localhost:8000`.

### extra

Arbitrary key-value pairs available in templates.

```toml
[project.extra]
key = "value"
```

## CLI Commands

### zensical new

```sh
zensical new [OPTIONS] PROJECT_DIRECTORY
```

Creates a new project at the given path.

### zensical serve

```sh
zensical serve [OPTIONS]
```

| Option | Short | Description |
|--------|-------|-------------|
| --config-file | -f | Path to config file |
| --open | -o | Open in default browser |
| --dev-addr IP:PORT | -a | Bind address (default: localhost:8000) |

### zensical build

```sh
zensical build [OPTIONS]
```

| Option | Short | Description |
|--------|-------|-------------|
| --config-file | -f | Path to config file |
| --clean | -c | Clean cache |

## Publishing

### GitHub Pages via GitHub Actions

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

Note: set `site_dir = "public"` in your config for GitLab.

## Upgrading

```sh
# pip
pip install --upgrade --force-reinstall zensical

# uv
uv lock --upgrade-package zensical==<version>
```

Zensical uses semantic versioning and is currently on 0.0.x (alpha).