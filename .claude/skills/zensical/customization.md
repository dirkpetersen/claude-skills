# Customization

## Additional CSS

Place CSS in `docs/stylesheets/extra.css`:

```css
:root {
  --md-primary-fg-color: #EE0F0F;
}
```

Register in config:

```toml
[project]
extra_css = ["stylesheets/extra.css"]
```

---

## Additional JavaScript

Place JS in `docs/javascripts/extra.js`:

```javascript
document$.subscribe(function() {
  console.log("Initialize third-party libraries here")
})
```

Register in config:

```toml
[project]
extra_javascript = ["javascripts/extra.js"]
```

### Module, async, defer

```toml
[[project.extra_javascript]]
path = "javascripts/extra.js"
type = "module"

[[project.extra_javascript]]
path = "javascripts/extra.js"
async = true
```

---

## Extending the Theme

Zensical uses MiniJinja templates. Set a `custom_dir` to override or add templates:

```toml
[project.theme]
custom_dir = "overrides"
```

Directory structure:

```sh
.
├─ overrides/
│  ├─ .icons/           # Custom icon sets
│  ├─ partials/         # Override partials (e.g. footer.html)
│  ├─ main.html         # Override main template
│  └─ 404.html          # Custom 404 page
└─ zensical.toml
```

---

## Overriding Blocks (recommended)

Create `overrides/main.html`:

```html
{% extends "base.html" %}

{% block htmltitle %}
  <title>Custom Title</title>
{% endblock %}
```

Use `{{ super() }}` to include original block content:

```html
{% extends "base.html" %}

{% block scripts %}
  <!-- Scripts before -->
  {{ super() }}
  <!-- Scripts after -->
{% endblock %}
```

Available blocks: `analytics`, `announce`, `config`, `container`, `content`, `extrahead`, `fonts`, `footer`, `header`, `hero`, `htmltitle`, `libs`, `outdated`, `scripts`, `site_meta`, `site_nav`, `styles`, `tabs`.

---

## Overriding Partials

Create a file at the same path under `overrides/`:

```sh
overrides/
└─ partials/
   └─ footer.html
```

---

## Custom Templates

Create a template in `overrides/` and reference it in front matter:

```yaml
---
template: my_template.html
---
```

Example template:

```html
{% extends "base.html" %}

{% block extrahead %}
  {% if page and page.meta and page.meta.robots %}
    <meta name="robots" content="{{ page.meta.robots }}" />
  {% else %}
    <meta name="robots" content="index, follow" />
  {% endif %}
{% endblock %}
```

---

## Custom Icons

Create `overrides/.icons/<set>/*.svg`, then register:

```toml
[project.theme]
custom_dir = "overrides"

[project.markdown_extensions.pymdownx.emoji]
emoji_index = "zensical.extensions.emoji.twemoji"
emoji_generator = "zensical.extensions.emoji.to_svg"
options.custom_icons = ["overrides/.icons"]
```

Use in config:

```toml
[project.theme.icon]
logo = "bootstrap/envelope-paper"
```

Use in Markdown:

```markdown
:bootstrap-envelope-paper:
```

---

## Custom Color Schemes

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

Tune the slate dark scheme hue:

```css
[data-md-color-scheme="slate"] {
  --md-hue: 210;
}
```

---

## Giscus Comment System

Override `overrides/partials/comments.html`:

```html
{% if page.meta.comments %}
  <h2 id="__comments">{{ lang.t("meta.comments") }}</h2>
  <!-- Insert Giscus generated snippet here -->
{% endif %}
```

Enable on a page:

```yaml
---
comments: true
---
```

---

## Custom Syntax Theme

Override code highlight colors in extra CSS:

```css
:root > * {
  --md-code-hl-string-color: #0FF1CE;
}
```

Target specific token class:

```css
.highlight .sb {
  color: #0FF1CE;
}
```

Annotation tooltip width:

```css
:root {
  --md-tooltip-width: 600px;
}