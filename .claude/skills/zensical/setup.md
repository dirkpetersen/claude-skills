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

---

## Creating a Project

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
- `docs/` — Markdown source files (`docs_dir` setting)
- `.github/` — GitHub Actions workflow for publishing

---

## Configuration File

Zensical uses `zensical.toml` (recommended for new projects) or `mkdocs.yml` (for migration from Material for MkDocs). All settings live under the `[project]` scope in TOML.

### Minimal configuration

```toml
[project]
site_name = "My site"
site_url = "https://example.com"
```

### Key settings

| Setting | Description |
| --- | --- |
| `site_name` | Required. Site title used in HTML head and headers. |
| `site_url` | Canonical URL; required for instant navigation, sitemaps, previews. |
| `site_description` | Meta description fallback. |
| `site_author` | Author meta tag. |
| `copyright` | Footer copyright notice (HTML allowed). |
| `docs_dir` | Source directory (default: `docs`). |
| `site_dir` | Output directory (default: `site`). |
| `use_directory_urls` | Controls URL format (default: `true`). Set `false` for offline. |
| `dev_addr` | Local server address (default: `localhost:8000`). |
| `repo_url` | Link to source repository. |
| `repo_name` | Repository display name. |
| `edit_uri` | Path component for edit/view buttons. |

### Theme variant

```toml
[project.theme]
variant = "classic"   # or "modern" (default)
```

`classic` matches the look and feel of Material for MkDocs. `modern` is the default new design.

### Navigation

Explicit navigation:

```toml
[project]
nav = [
  "index.md",
  {"Section" = [
    "section/index.md",
    "section/page.md"
  ]}
]
```

External links: any string that cannot resolve to a Markdown file is treated as a URL.

---

## CLI Commands

### `zensical new`

```sh
zensical new [OPTIONS] PROJECT_DIRECTORY
```

Creates a new project at the given path.

### `zensical build`

```sh
zensical build [OPTIONS]
```

| Option | Short | Description |
| --- | --- | --- |
| `--config-file` | `-f` | Path to config file |
| `--clean` | `-c` | Clean cache |
| `--help` | | Show help |

### `zensical serve`

```sh
zensical serve [OPTIONS]
```

Starts a local preview server (localhost:8000 by default).

| Option | Short | Description |
| --- | --- | --- |
| `--config-file` | `-f` | Path to config file |
| `--open` | `-o` | Open in default browser |
| `--dev-addr IP:PORT` | `-a` | Custom address |
| `--help` | | Show help |

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

### Upgrading

```sh
# pip
pip install --upgrade --force-reinstall zensical

# uv
uv lock --upgrade-package zensical==<version>