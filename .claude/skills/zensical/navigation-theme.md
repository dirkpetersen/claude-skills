# Navigation and Theme

## Navigation Features

Enable features via the `features` list:

```toml
[project.theme]
features = [
  "navigation.instant",
  "navigation.tabs",
  "navigation.sections",
  "navigation.expand",
  "navigation.path",
  "navigation.indexes",
  "navigation.top",
  "navigation.footer",
  "navigation.tracking",
  "navigation.prune",
  "toc.follow",
  "toc.integrate",
  "header.autohide",
  "announce.dismiss",
  "search.highlight",
  "content.code.copy",
  "content.code.select",
  "content.code.annotate",
  "content.tabs.link",
  "content.footnote.tooltips",
  "content.tooltips",
  "content.action.edit",
  "content.action.view"
]
```

### Instant Navigation

Intercepts internal link clicks and loads pages via XHR (Single Page Application behavior). Requires `site_url` to be set.

```toml
[project.theme]
features = ["navigation.instant"]
```

Sub-features:
- `navigation.instant.prefetch` — prefetch pages on hover
- `navigation.instant.progress` — show progress bar for slow loads

### Instant Previews

Show a preview tooltip for links using the `data-preview` attribute in Markdown:

```markdown
[Some page](other-page.md#section){ data-preview }
```

Enable automatically per-page/section:

```toml
[project.markdown_extensions.zensical.extensions.preview]
configurations = [
  { targets.include = ["setup/extensions/*"] }
]
```

### Navigation Tabs

Renders top-level sections as tabs below the header on wide viewports.

```toml
features = ["navigation.tabs"]
# Sticky tabs:
features = ["navigation.tabs", "navigation.tabs.sticky"]
```

### Navigation Sections

Renders top-level sections as groups in the sidebar.

```toml
features = ["navigation.sections"]
```

### Section Index Pages

Attach a document directly to a section by naming it `index.md` and placing it first in nav:

```toml
[project]
nav = [
  {"Section" = [
    "section/index.md",
    "section/page-1.md"
  ]}
]
```

Enable the feature:

```toml
features = ["navigation.indexes"]
```

### Other Navigation Features

| Feature | Effect |
| --- | --- |
| `navigation.expand` | Auto-expand all sidebar sections |
| `navigation.path` | Breadcrumb navigation above page title |
| `navigation.prune` | Only render visible nav items (reduces build size) |
| `navigation.top` | Back-to-top button |
| `navigation.footer` | Previous/next page links in footer |
| `navigation.tracking` | Update URL with active anchor |
| `toc.follow` | Auto-scroll sidebar to active anchor |
| `toc.integrate` | Move table of contents into left sidebar |

### Hiding Sidebars

In page front matter:

```yaml
---
hide:
  - navigation
  - toc
  - path
  - footer
  - tags
  - feedback
---
```

---

## Colors

### Color Scheme

```toml
[project.theme.palette]
scheme = "default"   # or "slate" for dark mode
```

### Primary and Accent Colors

```toml
[project.theme]
palette.primary = "indigo"
palette.accent = "indigo"
```

Available named colors: `red`, `pink`, `purple`, `deep-purple`, `indigo`, `blue`, `light-blue`, `cyan`, `teal`, `green`, `light-green`, `lime`, `yellow`, `amber`, `orange`, `deep-orange`, `brown`, `grey`, `blue-grey`, `black`, `white`.

### Color Palette Toggle (Light/Dark)

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

### System Preference

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

### Custom Colors

Set primary to `custom` and add CSS:

```toml
[project.theme.palette]
primary = "custom"

[project]
extra_css = ["stylesheets/extra.css"]
```

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

---

## Logo and Icons

```toml
[project.theme]
logo = "images/logo.png"          # image file
# or
[project.theme.icon]
logo = "lucide/smile"             # bundled icon
```

Favicon:

```toml
[project.theme]
favicon = "images/favicon.png"
```

Homepage override:

```toml
[project.extra]
homepage = "https://example.com"
```

### Included Icon Sets

- Lucide
- Material Design
- FontAwesome
- Octicons
- Simple Icons

### Admonition Icons

```toml
[project.theme.icon.admonition]
note = "octicons/tag-16"
warning = "octicons/alert-16"
# etc.
```

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

---

## Search

Search is enabled by default with no configuration needed.

### Search Highlighting

```toml
features = ["search.highlight"]
```

### Exclude from Search

Page-level (front matter):

```yaml
---
search:
  exclude: true
---
```

Section-level (requires Attribute Lists):

```markdown
## Section { data-search-exclude }
```

---

## Tags

Tags are supported by default. Add tags in front matter:

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
JavaScript = "js"

[project.theme.icon.tag]
default = "lucide/hash"
html = "fontawesome/brands/html5"
js = "fontawesome/brands/js"
```

---

## Analytics

### Google Analytics

```toml
[project.extra.analytics]
provider = "google"
property = "G-XXXXXXXXXX"
```

### Feedback Widget

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

## Footer

### Social Links

```toml
[[project.extra.social]]
icon = "fontawesome/brands/github"
link = "https://github.com/zensical"
name = "Zensical on GitHub"
```

### Copyright

```toml
[project]
copyright = "Copyright &copy; 2025 My Name"
```

### Remove Generator Notice

```toml
[project.extra]
generator = false
```

---

## Header

### Autohide

```toml
features = ["header.autohide"]
```

### Announcement Bar

Override the `announce` block in `overrides/main.html`:

```html
{% extends "base.html" %}

{% block announce %}
  Your announcement here
{% endblock %}
```

Add dismiss button: `features = ["announce.dismiss"]`

---

## Language

```toml
[project.theme]
language = "en"
direction = "ltr"   # or "rtl"
```

### Language Selector

```toml
[project.extra]
alternate = [
  { name = "English", link = "/en/", lang = "en" },
  { name = "Deutsch", link = "/de/", lang = "de" }
]
```

---

## Repository

```toml
[project]
repo_url = "https://github.com/zensical/zensical"
repo_name = "zensical/zensical"
edit_uri = "edit/main/docs/"
```

Content action buttons:

```toml
features = ["content.action.edit", "content.action.view"]
```

Repository icon:

```toml
[project.theme.icon]
repo = "fontawesome/brands/github"
```

---

## Offline Usage

```toml
[project.plugins.offline]
```

Set `use_directory_urls = false` when building for the file system. Disable instant navigation, analytics, repository info, and comment systems for offline builds.

---

## Data Privacy / Cookie Consent

```toml
[project.extra.consent]
title = "Cookie consent"
description = "We use cookies to recognize your visits..."
actions = ["accept", "manage"]
```

---

## Comment System (Giscus)

Override `overrides/partials/comments.html` and enable per page:

```yaml
---
comments: true
---