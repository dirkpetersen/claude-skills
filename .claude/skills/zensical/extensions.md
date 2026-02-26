# Extensions

## Default Configuration

Zensical activates a sensible default set of extensions automatically. To use the defaults, no explicit extension configuration is needed. The full expansion of the defaults:

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

To reset to MkDocs defaults (disable all):

```toml
[project]
markdown_extensions = {}
```

---

## Python Markdown Extensions

### Abbreviations

```toml
[project.markdown_extensions.abbr]
```

No options. Enables `*[ABBR]: Definition` syntax.

### Admonition

```toml
[project.markdown_extensions.admonition]
```

No options. Enables `!!! type` call-out blocks.

### Attribute Lists

```toml
[project.markdown_extensions.attr_list]
```

No options. Enables `{ .class #id attr=value }` syntax on elements.

### Definition Lists

```toml
[project.markdown_extensions.def_list]
```

No options. Enables `term\n:   definition` syntax.

### Footnotes

```toml
[project.markdown_extensions.footnotes]
```

No options. Enables `[^1]` reference and `[^1]: content` definition.

### Markdown in HTML

```toml
[project.markdown_extensions.md_in_html]
```

No options. Enables Markdown inside HTML elements with `markdown` attribute.

### Table of Contents

```toml
[project.markdown_extensions.toc]
permalink = true
permalink_title = "Anchor link to this section"
title = "On this page"
toc_depth = 3
```

Slugify option:

```toml
[project.markdown_extensions.toc.slugify]
object = "pymdownx.slugs.slugify"
kwds = { case = "lower" }
```

### Tables

```toml
[project.markdown_extensions.tables]
```

No options.

---

## Python Markdown Extensions (pymdownx)

### Arithmatex

```toml
[project.markdown_extensions.pymdownx.arithmatex]
generic = true
```

Enables math rendering with MathJax or KaTeX.

### Caption

```toml
[project.markdown_extensions.pymdownx.blocks.caption]
```

Adds captions to any Markdown block element.

### Caret, Mark, Tilde

```toml
[project.markdown_extensions.pymdownx.caret]
[project.markdown_extensions.pymdownx.mark]
[project.markdown_extensions.pymdownx.tilde]
```

Enables `^^underline^^`, `==highlight==`, `~~strikethrough~~`, `^super^`, `~sub~`.

### Details

```toml
[project.markdown_extensions.pymdownx.details]
```

Makes admonitions collapsible with `???` syntax.

### Emoji

```toml
[project.markdown_extensions.pymdownx.emoji]
emoji_index = "zensical.extensions.emoji.twemoji"
emoji_generator = "zensical.extensions.emoji.to_svg"
options.custom_icons = ["overrides/.icons"]
```

### Highlight

```toml
[project.markdown_extensions.pymdownx.highlight]
anchor_linenums = true
line_spans = "__span"
pygments_lang_class = true
auto_title = true
linenums = true
linenums_style = "pymdownx-inline"
```

### InlineHilite

```toml
[project.markdown_extensions.pymdownx.highlight]
[project.markdown_extensions.pymdownx.inlinehilite]
```

Enables `#!python code` inline syntax highlighting.

### Keys

```toml
[project.markdown_extensions.pymdownx.keys]
```

Enables `++ctrl+alt+del++` keyboard key rendering.

### SmartSymbols

```toml
[project.markdown_extensions.pymdownx.smartsymbols]
```

Converts character sequences to symbols (copyright, fractions, etc.).

### Snippets

```toml
[project.markdown_extensions.pymdownx.snippets]
auto_append = ["includes/abbreviations.md"]
```

Embeds content from other files with `--8<--` notation.

### SuperFences

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" }
]
```

Allows arbitrary nesting of code and content blocks.

### Tabbed

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

### mkdocstrings (API docs)

```toml
[project.plugins.mkdocstrings.handlers.python]
inventories = ["https://docs.python.org/3/objects.inv"]
paths = ["src"]

[project.plugins.mkdocstrings.handlers.python.options]
docstring_style = "google"
inherited_members = true
show_source = false
```

Install separately: `pip install mkdocstrings-python`