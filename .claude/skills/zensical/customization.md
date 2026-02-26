# Customization

## Additional CSS

Place a stylesheet in `docs/stylesheets/extra.css`:

```toml
[project]
extra_css = ["stylesheets/extra.css"]
```

## Additional JavaScript

Place a script in `docs/javascripts/extra.js`:

```toml
[project]
extra_javascript = ["javascripts/extra.js"]
```

### JavaScript Modules, async, defer

```toml
[[project.extra_javascript]]
path = "javascripts/extra.js"
type = "module"
async = true
```

### Running Code After Page Load

Use the `document$` observable for compatibility with instant navigation:

```js
document$.subscribe(function() {
  console.log("Initialize third-party libraries here")
})
```

## Extending the Theme

### Configure Overrides Directory

```toml
[project.theme]
custom_dir = "overrides"
```

### Theme File Structure

```sh
.
├─ .icons/
├─ assets/
│  ├─ images/
│  ├─ javascripts/
│  └─ stylesheets/
├─ partials/
│  ├─ integrations/analytics/
│  ├─ languages/
│  ├─ actions.html
│  ├─ comments.html
│  ├─ content.html
│  ├─ footer.html
│  ├─ header.html
│  ├─ nav.html
│  ├─ search.html
│  ├─ social.html
│  ├─ toc.html
│  └─ ... (other partials)
├─ 404.html
├─ base.html
└─ main.html
```

### Overriding Blocks (Recommended)

Create `overrides/main.html`:

```html
{% extends "base.html" %}

{% block htmltitle %}
  <title>Lorem ipsum dolor sit amet</title>
{% endblock %}
```

Include original block content:

```html
{% extends "base.html" %}

{% block scripts %}
  {{ super() }}
  <!-- Additional scripts -->
{% endblock %}
```

Available blocks: `analytics`, `announce`, `config`, `container`, `content`, `extrahead`, `fonts`, `footer`, `header`, `hero`, `htmltitle`, `libs`, `outdated`, `scripts`, `site_meta`, `site_nav`, `styles`, `tabs`.

### Overriding Partials

Create a file at the same path in `overrides/`:

```sh
overrides/
└─ partials/
   └─ footer.html
```

### Custom Templates

Create a template in `overrides/`, then reference it in page front matter:

```yaml
---
template: "my_template.html"
---
```

### Custom Error Pages

```sh
overrides/
└─ 404.html
```

### Use Front Matter in Templates

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

Page front matter:

```yaml
---
robots: noindex, nofollow
---