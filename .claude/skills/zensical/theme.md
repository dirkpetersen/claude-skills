# Theme

## Colors

### Color scheme

```toml
[project.theme.palette]
scheme = "default"   # light mode
# scheme = "slate"   # dark mode
```

### Primary and accent colors

```toml
[project.theme]
palette.primary = "indigo"
palette.accent = "indigo"
```

Available named colors: `red`, `pink`, `purple`, `deep-purple`, `indigo`, `blue`, `light-blue`, `cyan`, `teal`, `green`, `light-green`, `lime`, `yellow`, `amber`, `orange`, `deep-orange`, `brown`, `grey`, `blue-grey`, `black`, `white`.

### Color palette toggle (light/dark)

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

### System preference

```toml
[[project.theme.palette]]
media = "(prefers-color-scheme: light)"
scheme = "default"
toggle.icon = "lucide/sun"
toggle.name = "Switch to dark mode"

[[project.theme.palette]]
media = "(prefers-color-scheme: dark)"
scheme = "slate"
toggle.icon = "lucide/moon"
toggle.name = "Switch to light mode"
```

### Custom colors

Set `primary = "custom"` then add CSS:

```css
:root > * {
  --md-primary-fg-color:        #EE0F0F;
  --md-primary-fg-color--light: #ECB7B7;
  --md-primary-fg-color--dark:  #90030C;
}
```

---

## Fonts

```toml
[project.theme]
font.text = "Inter"
font.code = "JetBrains Mono"
```

Disable Google Fonts:

```toml
[project.theme]
font = false
```

Custom font via extra CSS:

```css
@font-face {
  font-family: "MyFont";
  src: "...";
}
:root {
  --md-text-font: "MyFont";
  --md-code-font: "MyFont";
}
```

---

## Logo and Icons

```toml
[project.theme]
logo = "images/logo.png"

[project.theme.icon]
logo = "lucide/smile"
```

Custom homepage for logo link:

```toml
[project.extra]
homepage = "https://example.com"
```

Favicon:

```toml
[project.theme]
favicon = "images/favicon.png"
```

Site icons (customizable):

```toml
[project.theme.icon]
previous = "fontawesome/solid/angle-left"
next = "fontawesome/solid/angle-right"
```

All customizable icon names: `logo`, `menu`, `alternate`, `search`, `share`, `close`, `top`, `edit`, `view`, `repo`, `admonition`, `tag`, `previous`, `next`.

---

## Navigation

### Feature flags

```toml
[project.theme]
features = [
  "navigation.instant",
  "navigation.instant.prefetch",
  "navigation.instant.progress",
  "navigation.tracking",
  "navigation.tabs",
  "navigation.tabs.sticky",
  "navigation.sections",
  "navigation.expand",
  "navigation.path",
  "navigation.prune",
  "navigation.indexes",
  "navigation.top",
  "navigation.footer",
  "toc.follow",
  "toc.integrate",
  "header.autohide",
  "announce.dismiss",
  "search.highlight",
  "content.code.copy",
  "content.code.select",
  "content.code.annotate",
  "content.tabs.link",
  "content.tooltips",
  "content.footnote.tooltips",
  "content.action.edit",
  "content.action.view"
]
```

### Instant navigation

Intercepts internal link clicks and loads pages via XHR (SPA behavior). Requires `site_url` to be set.

### Instant previews

Enable for specific pages/sections:

```toml
[[project.markdown_extensions.zensical.extensions.preview.configurations]]
targets.include = ["customization.md", "setup/extensions/*"]
```

Or add `data-preview` attribute to individual links in Markdown:

```markdown
[Link text](other-page.md#section){ data-preview }
```

### Section index pages

Name a file `index.md` inside a section folder and list it first in nav:

```toml
[project]
nav = [
  {"Section" = [
    "section/index.md",
    {"Page 1" = "section/page-1.md"}
  ]}
]
```

---

## Header

```toml
[project.theme]
features = ["header.autohide", "announce.dismiss"]
```

Announcement bar — override the `announce` block in a template:

```html
{% extends "base.html" %}
{% block announce %}
  Important announcement here
{% endblock %}
```

---

## Footer

```toml
[project.theme]
features = ["navigation.footer"]

[project]
copyright = "Copyright &copy; 2025 Example"

[project.extra]
generator = false   # hide "Made with Zensical" notice

[[project.extra.social]]
icon = "fontawesome/brands/github"
link = "https://github.com/example"
name = "GitHub"
```

---

## Search

Built-in, enabled by default, works offline. English only currently.

```toml
[project.theme]
features = ["search.highlight"]
```

Exclude a page from search (front matter):

```yaml
---
search:
  exclude: true
---
```

Exclude a section:

```markdown
## Section { data-search-exclude }
```

---

## Tags

```toml
[project.extra.tags]
HTML5 = "html"
JavaScript = "js"

[project.theme.icon.tag]
default = "lucide/hash"
html = "fontawesome/brands/html5"
js = "fontawesome/brands/js"
```

Add tags to a page (front matter):

```yaml
---
tags:
  - HTML5
  - JavaScript
---
```

---

## Analytics

### Google Analytics 4

```toml
[project.extra.analytics]
provider = "google"
property = "G-XXXXXXXXXX"
```

### Feedback widget

```toml
[project.extra.analytics.feedback]
title = "Was this page helpful?"

[[project.extra.analytics.feedback.ratings]]
icon = "material/emoticon-happy-outline"
name = "This page was helpful"
data = 1
note = "Thanks for your feedback!"

[[project.extra.analytics.feedback.ratings]]
icon = "material/emoticon-sad-outline"
name = "This page could be improved"
data = 0
note = "Thanks for your feedback!"
```

---

## Repository / Content Actions

```toml
[project]
repo_url = "https://github.com/example/repo"
repo_name = "example/repo"
edit_uri = "edit/main/docs/"

[project.theme]
features = ["content.action.edit", "content.action.view"]

[project.theme.icon]
repo = "fontawesome/brands/github"
edit = "material/pencil"
view = "material/eye"
```

---

## Cookie Consent

```toml
[project.extra.consent]
title = "Cookie consent"
description = "We use cookies to recognize your preferences."
actions = ["accept", "manage"]
```

Add a link to change cookie settings in the copyright notice:

```toml
[project]
copyright = """
  Copyright &copy; 2025 –
  <a href="#__consent">Change cookie settings</a>
"""
```

---

## Language

```toml
[project.theme]
language = "en"
direction = "ltr"

[project.extra]
alternate = [
  { name = "English", link = "/en/", lang = "en" },
  { name = "Deutsch", link = "/de/", lang = "de" }
]