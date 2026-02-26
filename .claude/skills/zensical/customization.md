# Customization

## Additional CSS

Place files in `docs/` and reference them:

```toml
[project]
extra_css = ["stylesheets/extra.css"]
```

Example — custom code highlight color:

```css
:root > * {
  --md-code-hl-string-color: #0FF1CE;
}
```

---

## Additional JavaScript

```toml
[project]
extra_javascript = ["javascripts/extra.js"]
```

Use `document$` observable for initialization (required for instant navigation):

```js
document$.subscribe(function() {
  console.log("Initialize third-party libraries here")
})
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

### Configure overrides directory

```toml
[project.theme]
custom_dir = "overrides"
```

Files in `overrides/` shadow theme files of the same name.

### Theme file structure

```sh
.
├─ .icons/
├─ assets/
│  ├─ images/
│  ├─ javascripts/
│  └─ stylesheets/
├─ partials/
│  ├─ footer.html
│  ├─ header.html
│  ├─ nav.html
│  ├─ search.html
│  ├─ comments.html
│  └─ ... (many more)
├─ 404.html
├─ base.html
└─ main.html
```

---

## Overriding Blocks (Recommended)

Create `overrides/main.html` extending `base.html`:

```html
{% extends "base.html" %}

{% block htmltitle %}
  <title>Custom Title</title>
{% endblock %}
```

Add to a block without replacing:

```html
{% extends "base.html" %}

{% block scripts %}
  {{ super() }}
  <script src="my-script.js"></script>
{% endblock %}
```

### Available template blocks

| Block | Purpose |
| --- | --- |
| `analytics` | Analytics integration |
| `announce` | Announcement bar |
| `config` | JS application config |
| `container` | Main content container |
| `content` | Main content |
| `extrahead` | Custom meta tags |
| `fonts` | Font definitions |
| `footer` | Footer bar |
| `header` | Fixed header bar |
| `htmltitle` | `<title>` tag |
| `libs` | JS libraries (header) |
| `scripts` | JS application (footer) |
| `site_meta` | Meta tags in `<head>` |
| `site_nav` | Navigation + TOC |
| `styles` | Style sheets |
| `tabs` | Tabs navigation |

---

## Overriding Partials

Copy the partial to the same relative path in `overrides/`:

```sh
overrides/
└─ partials/
   └─ footer.html
```

---

## Custom Templates

Create a template in `overrides/` with a unique name, then reference it in page front matter:

```yaml
---
template: my_homepage.html
---
```

Template file:

```html
{% extends "base.html" %}

{% block content %}
  <h1>Custom Layout</h1>
{% endblock %}
```

---

## Custom Error Pages

Create `overrides/404.html`:

```sh
overrides/
└─ 404.html
```

---

## Custom Metadata in Templates

Use front matter values in template overrides:

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
```

---

## Custom Colors (CSS Variables)

Code block colors:

```css
:root > * {
  --md-code-hl-number-color:      /* numbers */;
  --md-code-hl-special-color:     /* special */;
  --md-code-hl-function-color:    /* functions */;
  --md-code-hl-constant-color:    /* constants */;
  --md-code-hl-keyword-color:     /* keywords */;
  --md-code-hl-string-color:      /* strings */;
  --md-code-fg-color:             /* foreground */;
  --md-code-bg-color:             /* background */;
  --md-code-hl-color:             /* highlight line */;
}
```

Annotation tooltip width:

```css
:root {
  --md-tooltip-width: 600px;
}
```

---

## Custom Fonts

```css
@font-face {
  font-family: "MyFont";
  src: url("../fonts/myfont.woff2");
}

:root {
  --md-text-font: "MyFont";
  --md-code-font: "MyMonoFont";
}
```

---

## Custom Color Schemes

```css
[data-md-color-scheme="my-scheme"] {
  --md-primary-fg-color:        #EE0F0F;
  --md-primary-fg-color--light: #ECB7B7;
  --md-primary-fg-color--dark:  #90030C;
}
```

```toml
[project.theme.palette]
scheme = "my-scheme"