# Plugins and Integrations

## Offline Plugin

Makes site search work when documentation is distributed as a download.

```toml
[project.plugins.offline]
```

Disable for specific environments:

```toml
[project.plugins.offline]
enabled = false
```

When building offline, disable: instant navigation, site analytics, git repository, comment systems.

## mkdocstrings

Renders API reference documentation from source code docstrings.

### Installation

```sh
pip install mkdocstrings-python
```

### Configuration

```toml
[project.plugins.mkdocstrings.handlers.python]
inventories = ["https://docs.python.org/3/objects.inv"]
paths = ["src"]

[project.plugins.mkdocstrings.handlers.python.options]
docstring_style = "google"
inherited_members = true
show_source = false
```

Note: source paths outside the project directory are not watched for changes in `zensical serve`.

## Search

Built-in search is enabled by default. No configuration needed.

### Search Highlighting

```toml
[project.theme]
features = ["search.highlight"]
```

### Search Exclusion

Per-page:

```yaml
---
search:
  exclude: true
---
```

Per-section:

```markdown
## Section { data-search-exclude }
```

Per-block:

```markdown
Excluded content
{ data-search-exclude }
```

## Analytics — Google Analytics

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

#### Hide Feedback Widget per Page

```yaml
---
hide:
  - feedback
---
```

### Custom Analytics Integration

Create `overrides/partials/integrations/analytics/custom.html`:

```html
<script>
  var property = "{{ config.extra.analytics.property }}"
  document.addEventListener("DOMContentLoaded", function() {
    location$.subscribe(function(url) {
      /* custom page tracking */
    })
  })
</script>
```

```toml
[project.extra.analytics]
provider = "custom"
property = "foobar"
```

## Data Privacy — Cookie Consent

```toml
[project.extra.consent]
title = "Cookie consent"
description = """
  We use cookies to recognize your repeated visits and preferences.
"""
```

### Custom Cookie

```toml
[project.extra.consent.cookies]
analytics = "Google Analytics"
custom = "Custom cookie"
```

### Consent Actions

```toml
[project.extra.consent]
actions = ["accept", "manage"]
```

Actions: `accept`, `reject`, `manage`.

### Change Cookie Settings Link

```toml
[project]
copyright = """
  Copyright &copy; Zensical LLC –
  <a href="#__consent">Change cookie settings</a>
"""
```

### Custom Cookie in JavaScript

```js
var consent = __md_get("__consent")
if (consent && consent.custom) {
  /* accepted */
}
```

## Comment System — Giscus

1. Install the Giscus GitHub App and grant access to your repo.
2. Generate the snippet at giscus.app.
3. Create `overrides/partials/comments.html`:

```html
{% if page.meta.comments %}
  <h2 id="__comments">{{ lang.t("meta.comments") }}</h2>
  <!-- paste generated Giscus script tag here -->

  <script>
    var giscus = document.querySelector("script[src*=giscus]")
    var palette = __md_get("__palette")
    if (palette && typeof palette.color === "object") {
      var theme = palette.color.scheme === "slate"
        ? "transparent_dark" : "light"
      giscus.setAttribute("data-theme", theme)
    }
    document.addEventListener("DOMContentLoaded", function() {
      var ref = document.querySelector("[data-md-component=palette]")
      ref.addEventListener("change", function() {
        var palette = __md_get("__palette")
        if (palette && typeof palette.color === "object") {
          var theme = palette.color.scheme === "slate"
            ? "transparent_dark" : "light"
          var frame = document.querySelector(".giscus-frame")
          frame.contentWindow.postMessage(
            { giscus: { setConfig: { theme } } },
            "https://giscus.app"
          )
        }
      })
    })
  </script>
{% endif %}
```

Enable on a page:

```yaml
---
comments: true
---