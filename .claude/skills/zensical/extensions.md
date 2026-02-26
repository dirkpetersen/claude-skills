# Extensions

Zensical uses Python Markdown with Python Markdown Extensions. Configure them under `[project.markdown_extensions]` in `zensical.toml`.

## Default Configuration

Zensical enables a sensible set of extensions by default. To use the defaults, omit the `markdown_extensions` key. To reset to bare MkDocs defaults:

```toml
[project]
markdown_extensions = {}
```

Full default configuration:

```toml
[project.markdown_extensions.abbr]
[project.markdown_extensions.admonition]
[project.markdown_extensions.attr_list]
[project.markdown_extensions.def_list]
[project.markdown_extensions.footnotes]
[project.markdown_extensions.md_in_html]
[project.markdown_extensions.toc]
permalink = true
[project.markdown_extensions.pymdownx.arithmatex]
generic = true
[project.markdown_extensions.pymdownx.betterem]
smart_enable = "all"
[project.markdown_extensions.pymdownx.caret]
[project.markdown_extensions.pymdownx.details]
[project.markdown_extensions.pymdownx.emoji]
emoji_generator = "zensical.extensions.emoji.to_svg"
emoji_index = "zensical.extensions.emoji.twemoji"
[project.markdown_extensions.pymdownx.highlight]
[project.markdown_extensions.pymdownx.inlinehilite]
[project.markdown_extensions.pymdownx.keys]
[project.markdown_extensions.pymdownx.mark]
[project.markdown_extensions.pymdownx.smartsymbols]
[project.markdown_extensions.pymdownx.superfences]
[project.markdown_extensions.pymdownx.tabbed]
alternate_style = true
[project.markdown_extensions.pymdownx.tasklist]
custom_checkbox = true
[project.markdown_extensions.pymdownx.tilde]
```

---

## Python Markdown Extensions Reference

### Abbreviations (`abbr`)

```toml
[project.markdown_extensions.abbr]
```

No options. Use: `*[ABBR]: Definition`

### Admonition (`admonition`)

```toml
[project.markdown_extensions.admonition]
```

No options. Use `!!!` prefix syntax.

### Attribute Lists (`attr_list`)

```toml
[project.markdown_extensions.attr_list]
```

No options. Adds `{ .class #id key=value }` syntax to any element.

### Definition Lists (`def_list`)

```toml
[project.markdown_extensions.def_list]
```

No options. Use `:   definition` syntax.

### Footnotes (`footnotes`)

```toml
[project.markdown_extensions.footnotes]
```

No options. Use `[^id]` and `[^id]: content` syntax.

### Markdown in HTML (`md_in_html`)

```toml
[project.markdown_extensions.md_in_html]
```

No options. Add `markdown` attribute to HTML block elements.

### Table of Contents (`toc`)

```toml
[project.markdown_extensions.toc]
permalink = true
permalink_title = "Anchor link to this section"
title = "On this page"
toc_depth = 3
slugify = {object = "pymdownx.slugs.slugify", kwds = {case = "lower"}}
```

### Tables (`tables`)

```toml
[project.markdown_extensions.tables]
```

No options.

---

## Python Markdown Extensions (pymdownx) Reference

### Arithmatex

```toml
[project.markdown_extensions.pymdownx.arithmatex]
generic = true
```

### Caption

```toml
[project.markdown_extensions.pymdownx.blocks.caption]
```

### Caret / Mark / Tilde

```toml
[project.markdown_extensions.pymdownx.caret]
[project.markdown_extensions.pymdownx.mark]
[project.markdown_extensions.pymdownx.tilde]
```

### Details (collapsible admonitions)

```toml
[project.markdown_extensions.pymdownx.details]
```

### Emoji

```toml
[project.markdown_extensions.pymdownx.emoji]
emoji_index = "zensical.extensions.emoji.twemoji"
emoji_generator = "zensical.extensions.emoji.to_svg"
options.custom_icons = ["overrides/.icons"]
```

### Highlight (syntax highlighting)

```toml
[project.markdown_extensions.pymdownx.highlight]
anchor_linenums = true
line_spans = "__span"
pygments_lang_class = true
auto_title = true
linenums = true
linenums_style = "pymdownx-inline"
[project.markdown_extensions.pymdownx.superfences]
```

### InlineHilite

```toml
[project.markdown_extensions.pymdownx.highlight]
[project.markdown_extensions.pymdownx.inlinehilite]
```

### Keys

```toml
[project.markdown_extensions.pymdownx.keys]
```

Syntax: `++ctrl+alt+del++`

### SmartSymbols

```toml
[project.markdown_extensions.pymdownx.smartsymbols]
```

Converts sequences like `(c)` to ©.

### Snippets

```toml
[project.markdown_extensions.pymdownx.snippets]
auto_append = ["includes/abbreviations.md"]
```

Embed files with `;--8<-- "filename"` inside a code block.

### SuperFences

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" }
]
```

### Tabbed (content tabs)

```toml
[project.markdown_extensions.pymdownx.tabbed]
alternate_style = true
combine_header_slug = true
[project.markdown_extensions.pymdownx.tabbed.slugify]
object = "pymdownx.slugs.slugify"
kwds = { case = "lower" }
```

### Tasklist

```toml
[project.markdown_extensions.pymdownx.tasklist]
custom_checkbox = true
clickable_checkbox = false
```

---

## mkdocstrings (API Reference)

Install:

```sh
pip install mkdocstrings-python
```

Configure:

```toml
[project.plugins.mkdocstrings.handlers.python]
inventories = ["https://docs.python.org/3/objects.inv"]
paths = ["src"]

[project.plugins.mkdocstrings.handlers.python.options]
docstring_style = "google"
inherited_members = true
show_source = false