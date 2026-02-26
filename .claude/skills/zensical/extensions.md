# Extensions

Zensical uses Python Markdown and Python Markdown Extensions (PyMdown). A default set of extensions is active unless you override them.

## Default Configuration

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

To disable all defaults (reset to MkDocs behavior):

```toml
[project]
markdown_extensions = {}
```

## Python Markdown Extensions Reference

### abbr — Abbreviations

No config options. See [Authoring — Tooltips](authoring.md).

### admonition — Admonitions

No config options. See [Authoring — Admonitions](authoring.md).

### attr_list — Attribute Lists

No config options. Enables adding HTML attributes/CSS classes to elements.

### def_list — Definition Lists

No config options.

### footnotes — Footnotes

No config options.

### md_in_html — Markdown in HTML

No config options. Enables Markdown parsing inside HTML block elements when `markdown` attribute is present.

### toc — Table of Contents

```toml
[project.markdown_extensions.toc]
permalink = true
title = "On this page"
permalink = "⚓︎"
permalink_title = "Anchor link to this section"
toc_depth = 3
```

Slugify function:

```toml
[project.markdown_extensions.toc.slugify]
object = "pymdownx.slugs.slugify"
kwds = { case = "lower" }
```

### tables — Tables

No config options.

## PyMdown Extensions Reference

### pymdownx.arithmatex

```toml
[project.markdown_extensions.pymdownx.arithmatex]
generic = true
```

### pymdownx.blocks.caption

```toml
[project.markdown_extensions.pymdownx.blocks.caption]
```

### pymdownx.caret / mark / tilde

```toml
[project.markdown_extensions.pymdownx.caret]
[project.markdown_extensions.pymdownx.mark]
[project.markdown_extensions.pymdownx.tilde]
```

### pymdownx.details

```toml
[project.markdown_extensions.pymdownx.details]
```

### pymdownx.emoji

```toml
[project.markdown_extensions.pymdownx.emoji]
emoji_index = "zensical.extensions.emoji.twemoji"
emoji_generator = "zensical.extensions.emoji.to_svg"
options.custom_icons = ["overrides/.icons"]
```

### pymdownx.highlight

```toml
[project.markdown_extensions.pymdownx.highlight]
anchor_linenums = true
line_spans = "__span"
pygments_lang_class = true
auto_title = true
linenums = true
linenums_style = "pymdownx-inline"
```

### pymdownx.inlinehilite

```toml
[project.markdown_extensions.pymdownx.highlight]
[project.markdown_extensions.pymdownx.inlinehilite]
```

### pymdownx.keys

```toml
[project.markdown_extensions.pymdownx.keys]
```

### pymdownx.smartsymbols

```toml
[project.markdown_extensions.pymdownx.smartsymbols]
```

### pymdownx.snippets

```toml
[project.markdown_extensions.pymdownx.snippets]
auto_append = ["includes/abbreviations.md"]
```

### pymdownx.superfences

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" }
]
```

### pymdownx.tabbed

```toml
[project.markdown_extensions.pymdownx.tabbed]
alternate_style = true
combine_header_slug = true
```

Slugify:

```toml
[project.markdown_extensions.pymdownx.tabbed.slugify]
object = "pymdownx.slugs.slugify"
kwds = { case = "lower" }
```

### pymdownx.tasklist

```toml
[project.markdown_extensions.pymdownx.tasklist]
custom_checkbox = true
clickable_checkbox = true