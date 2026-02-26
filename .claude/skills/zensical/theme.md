# Theme

## Theme Variant

Zensical ships two variants: `modern` (default) and `classic` (matches Material for MkDocs).

```toml
[project.theme]
variant = "classic"
```

## Colors

### Color Scheme

```toml
[project.theme.palette]
scheme = "default"   # or "slate" for dark mode
```

### Primary Color

```toml
[project.theme]
palette.primary = "indigo"
```

Available: red, pink, purple, deep-purple, indigo, blue, light-blue, cyan, teal, green, light-green, lime, yellow, amber, orange, deep-orange, brown, grey, blue-grey, black, white.

### Accent Color

```toml
[project.theme]
palette.accent = "indigo"
```

### Color Palette Toggle (light/dark)

```toml
[[project.theme.palette]]
scheme = "default"
toggle.icon = "lucide/sun"
toggle.name = "Switch to dark mode"

[[project.theme.palette]]
scheme = "slate"
toggle.icon = "lucide/moon"
toggle.name = "Switch to light mode"
```

### System Preference / Auto Mode

```toml
[[project.theme.palette]]
media = "(prefers-color-scheme)"
toggle.icon = "lucide/sun-moon"
toggle.name = "Switch to light mode"

[[project.theme.palette]]
media = "(prefers-color-scheme: light)"
scheme = "default"
toggle.icon = "lucide/sun"
toggle.name = "Switch to dark mode"

[[project.theme.palette]]
media = "(prefers-color-scheme: dark)"
scheme = "slate"
toggle.icon = "lucide/moon"
toggle.name = "Switch to system preference"
```

### Custom Colors

Set primary to `"custom"` and override CSS variables in an extra stylesheet:

```toml
[project.theme.palette]
primary = "custom"
```

```css
:root > * {
  --md-primary-fg-color:        #EE0F0F;
  --md-primary-fg-color--light: #ECB7B7;
  --md-primary-fg-color--dark:  #90030C;
}
```

### Custom Color Schemes

```css
[data-md-color-scheme="youtube"] {
  --md-primary-fg-color:        #EE0F0F;
  --md-primary-fg-color--light: #ECB7B7;
  --md-primary-fg-color--dark:  #90030C;
}
```

```toml
[project]
theme.palette.scheme = "youtube"
extra_css = ["stylesheets/extra.css"]
```

## Fonts

### Regular Font

```toml
[project.theme]
font.text = "Inter"
```

### Monospaced Font

```toml
[project.theme]
font.code = "JetBrains Mono"
```

### Disable Google Fonts

```toml
[project.theme]
font = false
```

### Custom Fonts via CSS

```css
@font-face {
  font-family: "MyFont";
  src: "...";
}
:root {
  --md-text-font: "MyFont";
}
```

## Logo and Icons

### Logo from Image File

```toml
[project.theme]
logo = "images/logo.png"
```

### Logo from Bundled Icon

```toml
[project.theme.icon]
logo = "lucide/smile"
```

### Favicon

```toml
[project.theme]
favicon = "images/favicon.png"
```

### Site Icons

```toml
[project.theme.icon]
previous = "fontawesome/solid/angle-left"
next = "fontawesome/solid/angle-right"
```

Full list of customizable icon names: `logo`, `menu`, `alternate`, `search`, `share`, `close`, `top`, `edit`, `view`, `repo`, `admonition`, `tag`, `previous`, `next`.

### Additional Icons

Place SVG files in `overrides/.icons/<set>/*.svg`, then configure:

```toml
[project.theme]
custom_dir = "overrides"

[project.markdown_extensions.pymdownx.emoji]
emoji_index = "zensical.extensions.emoji.twemoji"
emoji_generator = "zensical.extensions.emoji.to_svg"
options.custom_icons = ["overrides/.icons"]
```

Use in Markdown: `:bootstrap-envelope-paper:`. Use in config: `bootstrap/envelope-paper`.

## Navigation

### Explicit Navigation

```toml
[project]
nav = [
  "index.md",
  {"About" = ["about/index.md", "about/team.md"]}
]
```

External links are any value that can't resolve to a Markdown file.

### Instant Navigation

```toml
[project.theme]
features = ["navigation.instant"]
```

Requires `site_url`. Enables SPA-style navigation without full page reload.

#### Instant Prefetching

```toml
[project.theme]
features = ["navigation.instant", "navigation.instant.prefetch"]
```

#### Progress Indicator

```toml
[project.theme]
features = ["navigation.instant", "navigation.instant.progress"]
```

### Instant Previews

Enable on a link with the `data-preview` attribute:

```markdown
[Attribute Lists](extensions/python-markdown.md#attribute-lists){ data-preview }
```

Automatic previews via extension:

```toml
[project.markdown_extensions.zensical.extensions.preview]
configurations = [
  { targets.include = ["customization.md", "setup/extensions/*"] }
]
```

### Anchor Tracking

```toml
[project.theme]
features = ["navigation.tracking"]
```

### Navigation Tabs

```toml
[project.theme]
features = ["navigation.tabs"]
```

Sticky tabs:

```toml
[project.theme]
features = ["navigation.tabs", "navigation.tabs.sticky"]
```

### Navigation Sections

```toml
[project.theme]
features = ["navigation.sections"]
```

### Navigation Expansion

```toml
[project.theme]
features = ["navigation.expand"]
```

### Navigation Path (Breadcrumbs)

```toml
[project.theme]
features = ["navigation.path"]
```

### Navigation Pruning

```toml
[project.theme]
features = ["navigation.prune"]
```

Reduces built site size by ~33%. Not compatible with `navigation.expand`.

### Section Index Pages

```toml
[project.theme]
features = ["navigation.indexes"]
```

Add `section/index.md` as the first item in a nav section.

### Table of Contents — Anchor Following

```toml
[project.theme]
features = ["toc.follow"]
```

### Table of Contents — Navigation Integration

```toml
[project.theme]
features = ["toc.integrate"]
```

### Back-to-Top Button

```toml
[project.theme]
features = ["navigation.top"]
```

### Hide Sidebars per Page

```yaml
---
hide:
  - navigation
  - toc
---
```

## Header

### Auto-Hide Header

```toml
[project.theme]
features = ["header.autohide"]
```

### Announcement Bar

Override the `announce` block in a template:

```html
{% extends "base.html" %}
{% block announce %}
  <!-- announcement HTML here -->
{% endblock %}
```

#### Dismissible Announcement

```toml
[project.theme]
features = ["announce.dismiss"]
```

## Footer

### Footer Navigation Links

```toml
[project.theme]
features = ["navigation.footer"]
```

### Social Links

```toml
[[project.extra.social]]
icon = "fontawesome/brands/github"
link = "https://github.com/zensical/zensical"
name = "Zensical on GitHub"
```

### Copyright Notice

```toml
[project]
copyright = "Copyright &copy; 2025 Zensical LLC"
```

### Remove Generator Notice

```toml
[project.extra]
generator = false
```

### Hide Footer Nav per Page

```yaml
---
hide:
  - footer
---
```

## Language

### Site Language

```toml
[project.theme]
language = "en"
```

### Language Selector

```toml
[project.extra]
alternate = [
  { name = "English", link = "/en/", lang = "en" },
  { name = "Deutsch", link = "/de/", lang = "de" }
]
```

### Directionality

```toml
[project.theme]
direction = "ltr"   # or "rtl"
```

## Repository

### Repository URL

```toml
[project]
repo_url = "https://github.com/zensical/zensical"
```

### Repository Name

```toml
[project]
repo_name = "zensical/zensical"
```

### Repository Icon

```toml
[project.theme.icon]
repo = "fontawesome/brands/github"
```

### Content Actions (Edit/View)

```toml
[project.theme]
features = ["content.action.edit", "content.action.view"]
```

### edit_uri

```toml
[project]
edit_uri = "edit/main/docs/"
```

## Tags

Tags are supported by default. Add to page front matter:

```yaml
---
tags:
  - HTML5
  - JavaScript
---
```

### Tag Icons

```toml
[project.extra.tags]
HTML5 = "html"

[project.theme.icon.tag]
default = "lucide/hash"
html = "fontawesome/brands/html5"
```

### Hide Tags per Page

```yaml
---
hide:
  - tags
---